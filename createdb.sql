create table users(
    id serial primary key,
    name varchar(255),
    address varchar(255)
);

create table rooms(
    id serial primary key,
    name varchar(255)
);

create table users_rooms(
    room_id int references rooms(id),
    user_id int references users(id)
);
