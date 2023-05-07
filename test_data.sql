INSERT INTO airline
VALUES ("China Eastern Airlines"), ("China Southern Airlines"),
        ("Air China");

INSERT INTO airport
VALUES ("JFK", "NYC"), ("PVG", "Shanghai"), ("PEK", "Beijing"),
       ("SHA", "Shanghai"), ("PKX", "Beijing"),("CSX", "Changsha"),
       ("CTU", "Chengdu"), ("CKG", "Chongqing"), ("FOC", "Fuzhou"), ("CAN", "Guangzhou");

INSERT INTO airplane
VALUES ("China Eastern Airlines", 330200, 247), 
        ("China Eastern Airlines", 330300, 277),
       ("China Southern Airlines", 330200, 247), 
       ("China Southern Airlines", 330300, 277);

INSERT INTO flight
VALUES  ("China Eastern Airlines", 0001, "PVG", "2021-05-01 08:00:00", "PEK", "2021-05-01 10:00:00", 1250, "Finished", 330300),
        ("China Eastern Airlines", 0002, "PVG", "2021-05-01 09:00:00", "PKX", "2021-05-01 11:00:00", 2500, "Finished", 330200),
        ("China Eastern Airlines", 0003, "SHA", "2023-05-12 10:00:00", "PEK", "2023-05-12 12:00:00", 999, "Upcoming", 330200),
        ("China Eastern Airlines", 0004, "SHA", "2023-05-12 11:00:00", "PKX", "2023-05-12 13:00:00", 1230, "Upcoming", 330200),
        ("China Eastern Airlines", 0005, "PEK", "2023-05-12 12:00:00", "PVG", "2023-05-12 14:00:00", 670, "Upcoming", 330300),
        ("China Eastern Airlines", 0006, "PEK", "2023-05-12 13:00:00", "SHA", "2023-05-12 15:00:00", 1000, "Upcoming", 330200),
        ("China Eastern Airlines", 0007, "PKX", "2023-06-01 14:00:00", "PVG", "2023-06-01 16:00:00", 3000, "Upcoming", 330200),
        ("China Eastern Airlines", 0008, "PKX", "2023-06-01 15:00:00", "SHA", "2023-06-01 17:00:00", 1470, "Upcoming", 330300),
        ("China Eastern Airlines", 0009, "CTU", "2023-05-17 21:30:00", "CSX", "2023-05-17 23:30:00", 1760, "Upcoming", 330300),
        ("China Southern Airlines", 1001, "PVG", "2021-05-01 08:00:00", "PEK", "2021-05-01 10:00:00", 1250, "Finished", 330300),
        ("China Southern Airlines", 1002, "PVG", "2021-05-01 09:00:00", "PKX", "2021-05-01 11:00:00", 2500, "Finished", 330200),
        ("China Southern Airlines", 1003, "SHA", "2023-05-12 10:00:00", "PEK", "2023-05-12 12:00:00", 999, "Upcoming", 330200),
        ("China Southern Airlines", 1004, "SHA", "2023-05-12 11:00:00", "PKX", "2023-05-12 13:00:00", 1230, "Upcoming", 330200),
        ("China Southern Airlines", 1005, "PEK", "2023-05-12 12:00:00", "PVG", "2023-05-12 14:00:00", 670, "Upcoming", 330300),
        ("China Southern Airlines", 1006, "PEK", "2023-05-12 13:00:00", "SHA", "2023-05-12 15:00:00", 1000, "Upcoming", 330200),
        ("China Southern Airlines", 1007, "PKX", "2023-06-01 14:00:00", "PVG", "2023-06-01 16:00:00", 3000, "Upcoming", 330200),
        ("China Southern Airlines", 1008, "PKX", "2023-06-01 15:00:00", "SHA", "2023-06-01 17:00:00", 1470, "Upcoming", 330300),
        ("China Southern Airlines", 1009, "CTU", "2023-05-17 21:30:00", "CSX", "2023-05-17 23:30:00", 1760, "Upcoming", 330300);
INSERT INTO airline_staff
VALUES  ("txr","txrtxr","tian","xiaorong","1998-09-09","China Eastern Airlines");

INSERT INTO permission
VALUES  ("txr","Admin");