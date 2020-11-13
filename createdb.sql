create table clients(
    id serial primary key,
    name varchar(255),
    addr varchar(50)
);

create table rooms(
    id serial primary key,
    name varchar(255),
    author_id int references clients(id)
);

create table clients_rooms(
    client_id int references clients(id) on update cascade,
    room_id int references rooms(id) on update cascade,
    constraint clients_rooms_pkey primary key (client_id, room_id)
);

create table messages(
    id serial primary key,
    room_id int references rooms(id),
    from_id int references clients(id),
    to_id int references clients(id),
    date_time timestamp default current_timestamp,
    content varchar(255)
);
