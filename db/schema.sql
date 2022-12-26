SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: member_to_role_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.member_to_role_map (
    id integer NOT NULL,
    member_username text NOT NULL,
    role_name text NOT NULL
);


--
-- Name: member_to_role_map_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.member_to_role_map_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: member_to_role_map_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.member_to_role_map_id_seq OWNED BY public.member_to_role_map.id;


--
-- Name: members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.members (
    username text NOT NULL,
    display_name text NOT NULL,
    is_member boolean DEFAULT false,
    region text,
    timezone integer
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    name text NOT NULL
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(255) NOT NULL
);


--
-- Name: member_to_role_map id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.member_to_role_map ALTER COLUMN id SET DEFAULT nextval('public.member_to_role_map_id_seq'::regclass);


--
-- Name: member_to_role_map member_to_role_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.member_to_role_map
    ADD CONSTRAINT member_to_role_map_pkey PRIMARY KEY (id);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (username);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (name);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: member_to_role_map member_to_role_map_member_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.member_to_role_map
    ADD CONSTRAINT member_to_role_map_member_username_fkey FOREIGN KEY (member_username) REFERENCES public.members(username);


--
-- Name: member_to_role_map member_to_role_map_role_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.member_to_role_map
    ADD CONSTRAINT member_to_role_map_role_name_fkey FOREIGN KEY (role_name) REFERENCES public.roles(name);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20220727065002');
