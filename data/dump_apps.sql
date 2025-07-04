-- shows_venue doesn't have a publish column
.dump shows_venue

.schema shows_gig
.mode insert shows_gig
SELECT * FROM shows_gig WHERE publish = 1;

.schema music_release
.mode insert music_release
SELECT * FROM music_release WHERE publish = 1;

.schema music_song
.mode insert music_song
SELECT * FROM music_song WHERE publish = 1;

.schema music_video
.mode insert music_video
SELECT * FROM music_video WHERE publish = 1;

.schema music_press
.mode insert music_press
SELECT * FROM music_press WHERE publish = 1;

.schema news_post
.mode insert news_post
SELECT * FROM news_post WHERE publish = 1;
