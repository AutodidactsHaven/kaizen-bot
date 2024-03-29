-- migrate:up

create table members(
    username text primary key,
    display_name text not null,
    is_member boolean default false,
    region text,
    timezone integer
);

create table roles(
    name text primary key
);

create table member_to_role_map(
    id serial primary key,
    member_username text not null references members(username),
    role_name text not null references roles(name)
);

-- migrate:down

drop table member_to_role_map;
drop table roles;
drop table members;