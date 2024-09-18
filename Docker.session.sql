select * from information_schema.tables


select * from public.user

DELETE FROM public.user WHERE id = 2

SELECT * FROM public.downlods
DELETE  FROM downlods

SELECT * FROM public.song WHERE song_id in(7,6)



UPDATE public.songs set link='' where song_id=4
UPDATE public.songs set link='/downloads/Nantes.mp3' where song_id = 7738

SELECT * FROM public.song where song_id = 4

SELECT * FROM public.songs where user_id =3


UPDATE public.songs set link = '//www.youtube.com/embed/9bZkp7q19f0?autoplay=1&mute=0' where id=40


DELETE  FROM public.songs where user_id =2




SELECT * FROM public.songs WHERE user_id not in (SELECT id FROM public.user)

SELECT * FROM public.alembic_version
DELETE FROM public.alembic_version


