/* creates tables for clients, commands, server info */
CREATE TABLE Server(
    ServerID integer primary key AUTO_INCREMENT,
    isActive integer not null,
    IPAddress varchar(15) not null,
    PortNumber integer not null,
    check (isActive in (0, 1))
);
\
CREATE TABLE Client(
    ClientID varchar(32) primary key,
    HostName varchar(256),
    ServerID integer,
    constraint FK foreign key(ServerID) references Server(ServerID)
);
\
CREATE TABLE Command(
    CommandID varchar(32) primary key,
    Command varchar(256) not null
);
\
CREATE TABLE ClientCommand(
    ClientID varchar(32),
    CommandID varchar(32),
    Sent integer,
    Result varchar(256),
    primary key (ClientID, CommandID),
    constraint FK_1 foreign key(ClientID) references Client(ClientID),
    constraint FK_2 foreign key(CommandID) references Command(CommandID)
);
\
