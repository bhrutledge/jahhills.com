import json
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from hth.music.models import Press, Release


class Command(BaseCommand):
    help = 'Import press items from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file containing press items')
        parser.add_argument('-r', '--release', type=str, help='Release slug to associate press items with')
        parser.add_argument('-p', '--publish', action='store_true', help='Mark imported press items as published')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be imported without saving')

    def handle(self, *args, **options):
        json_file = options['json_file']
        release_slug = options.get('release')
        publish = options['publish']
        dry_run = options['dry_run']

        # Get release if specified
        release = None
        if release_slug:
            try:
                release = Release.objects.get(slug=release_slug)
                self.stdout.write(f"Found release: {release.title}")
            except Release.DoesNotExist:
                raise CommandError(f'Release with slug "{release_slug}" does not exist')

        # Read and parse JSON file
        try:
            with open(json_file, 'r') as f:
                press_items = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'File "{json_file}" not found')
        except json.JSONDecodeError as e:
            raise CommandError(f'Invalid JSON in file: {e}')

        if not isinstance(press_items, list):
            raise CommandError('JSON file must contain an array of press items')

        if not press_items:
            self.stdout.write('No press items found in file')
            return

        # Validate required fields
        required_fields = ['title', 'date', 'source_url', 'body']
        for i, item in enumerate(press_items, 1):
            missing_fields = [field for field in required_fields if field not in item or not item[field]]
            if missing_fields:
                raise CommandError(f'Item {i} missing required fields: {", ".join(missing_fields)}')

        # Parse dates and create Press objects
        press_objects = []
        for i, item in enumerate(press_items, 1):
            try:
                # Parse date (expects YYYY-MM-DD format)
                date = datetime.strptime(item['date'], '%Y-%m-%d').date()
            except ValueError:
                raise CommandError(f'Item {i}: Invalid date format. Use YYYY-MM-DD')

            # Use quote value from JSON if provided, otherwise default to True
            is_quote = item.get('quote', True)

            press_obj = Press(
                title=item['title'],
                date=date,
                source_url=item['source_url'],
                body=item['body'],
                quote=is_quote,
                publish=publish,
                release=release
            )
            press_objects.append(press_obj)

        # Show what will be imported
        self.stdout.write(f'\nFound {len(press_objects)} press items to import:')
        for press_obj in press_objects:
            status = "PUBLISHED" if press_obj.publish else "DRAFT"
            release_info = f" (for {press_obj.release.title})" if press_obj.release else ""
            self.stdout.write(f'  - {press_obj.title} ({press_obj.date}) [{status}]{release_info}')

        if dry_run:
            self.stdout.write('\n[DRY RUN] No items were saved to database')
            return

        # Save to database
        with transaction.atomic():
            created_count = 0
            for press_obj in press_objects:
                # Check for duplicates based on title and date
                existing = Press.objects.filter(title=press_obj.title, date=press_obj.date).first()
                if existing:
                    self.stdout.write(f'  Skipping duplicate: {press_obj.title} ({press_obj.date})')
                    continue
                
                press_obj.save()
                created_count += 1

        success_msg = f'Successfully imported {created_count} press items'
        if created_count != len(press_objects):
            success_msg += f' ({len(press_objects) - created_count} duplicates skipped)'
        
        self.stdout.write(self.style.SUCCESS(success_msg))