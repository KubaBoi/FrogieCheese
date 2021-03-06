BEGIN;

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE IF NOT EXISTS public.users
(
    email text NOT NULL,
    picture_id bigint NOT NULL,
    id bigint NOT NULL,
    user_name text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.chats
(
    id bigint NOT NULL,
    last_activity bigint NOT NULL,
    chat_name text NOT NULL,
    picture_id bigint,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.chats_t
(
    user_id bigint NOT NULL,
    chat_id bigint NOT NULL,
    last_delivered_message_id bigint,
    last_seen_message_id bigint,
    id bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.groups
(
    id bigint NOT NULL,
    group_name text NOT NULL,
    chat_id bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.groups_t
(
    user_id bigint NOT NULL,
    group_id bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS public.messages
(
    id bigint NOT NULL,
    author_id bigint NOT NULL,
    content text NOT NULL,
    chat_id bigint NOT NULL,
    time_stamp bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.tokens
(
    token text NOT NULL,
    user_id bigint NOT NULL,
    ip text NOT NULL,
    end_time bigint NOT NULL,
    id bigint,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.passwords
(
    user_id bigint NOT NULL,
    password text NOT NULL,
    duration bigint NOT NULL,
    id bigint NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE public.chats_t
    ADD FOREIGN KEY (user_id)
    REFERENCES public.users (id)
    NOT VALID;


ALTER TABLE public.chats_t
    ADD FOREIGN KEY (chat_id)
    REFERENCES public.chats (id)
    NOT VALID;


ALTER TABLE public.groups
    ADD FOREIGN KEY (chat_id)
    REFERENCES public.chats (id)
    NOT VALID;


ALTER TABLE public.tokens
    ADD FOREIGN KEY (user_id)
    REFERENCES public.users (id)
    NOT VALID;


ALTER TABLE public.groups_t
    ADD FOREIGN KEY (user_id)
    REFERENCES public.users (id)
    NOT VALID;


ALTER TABLE public.groups_t
    ADD FOREIGN KEY (group_id)
    REFERENCES public.groups (id)
    NOT VALID;


ALTER TABLE public.messages
    ADD FOREIGN KEY (chat_id)
    REFERENCES public.chats (id)
    NOT VALID;


ALTER TABLE public.chats_t
    ADD FOREIGN KEY (last_delivered_message_id)
    REFERENCES public.messages (id)
    NOT VALID;


ALTER TABLE public.chats_t
    ADD FOREIGN KEY (last_seen_message_id)
    REFERENCES public.messages (id)
    NOT VALID;


ALTER TABLE public.passwords
    ADD FOREIGN KEY (user_id)
    REFERENCES public.users (id)
    NOT VALID;

END;