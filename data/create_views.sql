create view us_venues as
select * from shows_venue
where longitude between -124.7844079 and -66.9513812
and latitude between 24.7433195 and 49.3457868;

create view published_gigs as
select * from shows_gig where publish;

create view published_releases as
select * from music_release where publish;

create view published_songs as
select * from music_song where publish;

create view published_videos as
select * from music_video where publish;

create view published_press as
select * from music_press where publish;

create view published_posts as
select * from news_post where publish;
