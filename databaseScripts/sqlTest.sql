
insert into users (email, picture_id, id, user_name) values ('email', 0, 0, 'Kuba');
insert into users (email, picture_id, id, user_name) values ('email', 0, 1, 'Frank');
insert into users (email, picture_id, id, user_name) values ('email', 0, 2, 'Martin');

insert into passwords (id, user_id, password, duration) values (0, 0, 'heslo', 15151);
insert into passwords (id, user_id, password, duration) values (1, 0, 'heslo1', 15151000000);
insert into passwords (id, user_id, password, duration) values (2, 1, 'heslo', 15151);
insert into passwords (id, user_id, password, duration) values (5, 1, 'heslo1', 15151000000);
insert into passwords (id, user_id, password, duration) values (3, 2, 'heslo', 15151);
insert into passwords (id, user_id, password, duration) values (4, 2, 'heslo1', 15151000000);

insert into chats (id, last_activity, chat_name) values (0, 5, 'Kuba, Frank'); --chat Kuba and Frank
insert into chats (id, last_activity, chat_name) values (1, 15, 'Kuba, Martin'); --chat Kuba and Martin
insert into chats (id, last_activity, chat_name) values (2, 30, 'Frank, Martin'); --chat Frank and Martin

insert into chats_t (id, user_id, chat_id) values (0, 0, 0); --chat Kuba and Frank
insert into chats_t (id, user_id, chat_id) values (1, 1, 0); --chat Frank and Kuba

insert into chats_t (id, user_id, chat_id) values (2, 0, 1); --chat Kuba and Martin
insert into chats_t (id, user_id, chat_id) values (3, 2, 1); --chat Martin and Kuba

insert into chats_t (id, user_id, chat_id) values (4, 1, 2); --chat Frank and Martin
insert into chats_t (id, user_id, chat_id) values (5, 2, 2); --chat Martin and Frank

--tu

insert into messages (id, author_id, content, chat_id, time_stamp) 
	values (0, 0, 'ahoj kamo', 0, 1); --message for chat Kuba and Frank
insert into messages (id, author_id, content, chat_id, time_stamp) 
	values (2, 1, 'cus borce', 0, 2); --message for chat Kuba and Frank
insert into messages (id, author_id, content, chat_id, time_stamp)  
	values (3, 0, 'mas rad kozy?', 0, 3); --message for chat Kuba and Frank
insert into messages (id, author_id, content, chat_id, time_stamp)  
	values (6, 1, 'jo mam', 0, 4); --message for chat Kuba and Frank
	
insert into messages (id, author_id, content, chat_id, time_stamp)  
	values (1, 0, 'cus martine', 1, 4); --message for chat Kuba and Martin
	
insert into messages (id, author_id, content, chat_id, time_stamp) 
	values (4, 1, 'cus franku tady martin', 2, 5); --message for chat Frank and Martin
insert into messages (id, author_id, content, chat_id, time_stamp)  
	values (5, 2, 'cus martine tady frank', 2, 6); --message for chat Frank and Martin


insert into tokens (token, user_id, ip, end_time) values ('token0', 0, '1.1', 0);
insert into tokens (token, user_id, ip, end_time) values ('token1', 0, '1.2', 0);
insert into tokens (token, user_id, ip, end_time) values ('token2', 1, '1.1', 0);
insert into tokens (token, user_id, ip, end_time) values ('token3', 1, '1.0', 0);


--SELECTS

select * from users;
select * from chats where id = 0;
select * from chats_t where chat_id = 1;
select * from messages where chat_id = 1;
select * from tokens;
select * from passwords;

select * from chats where id in (0, 2);

select ct.id, ct.user_id, ct.chat_id, ct.last_delivered_message_id, ct.last_seen_message_id from chats_t ct
                    where ct.user_id = 1 and
                    (ct.last_delivered_message_id is NULL or
                    exists
                    (select ct2.id from chats_t ct2
                    inner join messages m
                    	on m.id = ct2.last_delivered_message_id
                    where ct2.user_id = 0 and exists
                    (select m2.id from messages m2
                    where m2.time_stamp > m.time_stamp and m2.chat_id = ct2.chat_id)))



--returns valid password
select * from passwords p
	inner join users u
		on u.id = p.user_id
	where p.password = 'heslo1' and p.duration > 1636452983 and u.user_name = 'Kuba';

--returns chat_ids for user with id 0 - Kuba
select chat_id from users inner join chats_t on users.id = user_id where users.id = 0;

--returns all chats of user with id 0 - Kuba
select c.id, chat_name, last_activity, c.picture_id from chats c
	inner join chats_t ct
		on ct.chat_id = c.id
	inner join users u
		on u.id = ct.user_id
	where u.id = 0;
	
--returns 2 chats fo user with id 0 - Kuba from lastActivity 20
select c.id, chat_name, last_activity, c.picture_id from chats c
	inner join chats_t ct
		on ct.chat_id = c.id
	inner join users u
		on u.id = ct.user_id
	where u.id = 0 and c.last_activity <= 39
	order by c.last_activity desc
	limit 2;

--returns all messages from all chats for user with id = 0 - Kuba
select m.id, author_id, content, m.chat_id, m.time_stamp from messages m
	inner join chats c
		on c.id = m.chat_id
	inner join chats_t ct
		on ct.chat_id = c.id
	inner join users u
		on u.id = ct.user_id
	where u.id = 0;
	
--returns all messages from chat with id = 0 for user with id = 0 - Kuba
select m.id, author_id, content, m.chat_id, m.time_stamp from messages m
	inner join chats c
		on c.id = m.chat_id
	inner join chats_t ct
		on ct.chat_id = c.id
	inner join users u
		on u.id = ct.user_id
	where u.id = 0 and c.id = 0;
	
--returns all messages from chat with id = 0 from time_stamp 2
select distinct m.id, author_id, content, m.chat_id, m.time_stamp from messages m
	inner join chats c
		on c.id = m.chat_id
	inner join chats_t ct
		on ct.chat_id = c.id
	inner join users u
		on u.id = ct.user_id
	where c.id = 0 and m.time_stamp <= 3
order by m.time_stamp desc
limit 2;
	
--returns token for user with token = 'token0' and ip = '1.0'
select u.id, user_name, picture_id, email from users u
	inner join tokens t
		on t.user_id = u.id
	where t.token = 'token3' and t.ip = '1.0';
	
--returns chat for user with id 0 and user with id 1
select c.id, chat_name, last_activity, c.picture_id from users u1
	inner join chats_t ct1 
		on u1.id = ct1.user_id
	inner join chats_t ct2
		on ct2.chat_id = ct1.chat_id
	inner join users u2
		on u2.id = ct2.user_id
	inner join chats c
		on c.id = ct2.chat_id
	where u1.id = 0 and u2.id = 2;

--does chat exists?
select * from users;

select case when exists
	(select * from users u1
	inner join chats_t ct1 
		on u1.id = ct1.user_id
	inner join chats_t ct2
		on ct2.chat_id = ct1.chat_id
	inner join users u2
		on u2.id = ct2.user_id
	inner join chats c
		on c.id = ct2.chat_id
	where u1.id = 0 and u2.id = 2)
then cast(1 as bit)
else cast(0 as bit) end;

--returns count of chats
select count(*) from chats;

--chat with id 0 belongs to user with id 0
select case when exists
	(select * from chats_t ct
	where ct.user_id = 0 and ct.chat_id = 0)
then cast(1 as bit)
else cast(0 as bit) end;

--findUndeliveredChatsByUserId(userId 0)
update chats_t set last_seen_message_id = NULL;
update chats_t set last_delivered_message_id = 3 where chat_id = 0;
select * from chats_t;
select * from messages;
select * from chats;

select ct.id, ct.user_id, ct.chat_id, ct.last_delivered_message_id, ct.last_seen_message_id from chats_t ct
	where ct.user_id = 0 and
	(ct.last_delivered_message_id is NULL or 
	exists (
		select * from chats_t ct2
		inner join messages m
			on m.id = ct2.last_delivered_message_id
		where ct2.user_id = 0 and exists 
			(select * from messages m2
			where m2.time_stamp > m.time_stamp and m2.chat_id = ct2.chat_id)));
		
--setLastSeen(userId 0, messageId 2, chatId 0)
update chats_t set last_seen_message_id = 2 
	where user_id = 0 and chat_id = 0;
	
--findUserByCredentials(userName 'Kuba', password 'heslo')
select * from users u where u.user_name = 'Kuba' and u.password = 'heslo';

--dynamic user search
select * from users;

select * from users where user_name like 'Kub%';


	



