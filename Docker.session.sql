select * from information_schema.tables


select * from public.user

DELETE FROM public.user WHERE id = 2

git


SELECT * FROM public.song


UPDATE public.song set link='//www.youtube.com/embed/9bZkp7q19f0?autoplay=1&mute=0' where song_id = 9


SELECT * FROM public.songs where user_id in ( 1,2,3)


UPDATE public.songs set link = '//www.youtube.com/embed/9bZkp7q19f0?autoplay=1&mute=0' where id=40


DELETE  FROM public.songs where user_id =2


SELECT * FROM public.songs WHERE user_id not in (SELECT id FROM public.user)