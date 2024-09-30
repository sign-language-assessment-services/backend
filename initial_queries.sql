INSERT INTO assessments VALUES ('c4d129f9-41da-4a79-9f24-b9d79f1e86aa', now(), 'SLAS DSGS GV');

INSERT INTO multimedia_files VALUES ('28669db7-9c97-422c-a7b7-afd3b5a964a5', now(), 'slportal', 'SLAS DSGS GV/00/00_1_1_Einführung.mp4', 'VIDEO');
INSERT INTO multimedia_files VALUES ('9cc09540-dd71-456b-a311-8ae187849d72', now(), 'slportal', 'SLAS DSGS GV/03/01_Frage.mp4', 'VIDEO');
INSERT INTO multimedia_files VALUES ('9feab952-0730-433a-9c36-78080f29b3d4', now(), 'slportal', 'SLAS DSGS GV/03/01a_Antwort.mp4', 'VIDEO');
INSERT INTO multimedia_files VALUES ('2d8f4f20-4bd2-42ec-add4-30adbf8f9132', now(), 'slportal', 'SLAS DSGS GV/03/01b_Antwort.mp4', 'VIDEO');
INSERT INTO multimedia_files VALUES ('bee674ed-4440-488d-b22f-1a00ac77952c', now(), 'slportal', 'SLAS DSGS GV/03/01c_Antwort_richtig.mp4', 'VIDEO');

INSERT INTO primers VALUES ('ace257e6-85d9-4017-9e7c-645a3812c8fc', now(), 0, 'c4d129f9-41da-4a79-9f24-b9d79f1e86aa', '28669db7-9c97-422c-a7b7-afd3b5a964a5');
INSERT INTO exercises VALUES ('d24b2d12-dcac-4747-8d94-84b7002df647', now(), 1, 'c4d129f9-41da-4a79-9f24-b9d79f1e86aa', '9cc09540-dd71-456b-a311-8ae187849d72');

INSERT INTO choices VALUES ('e57175a9-ff4e-4368-bc14-8156c252274d', now(), false, 'd24b2d12-dcac-4747-8d94-84b7002df647', '9feab952-0730-433a-9c36-78080f29b3d4');
INSERT INTO choices VALUES ('216c487a-a9e7-481b-8475-bb9f1ec3418b', now(), false, 'd24b2d12-dcac-4747-8d94-84b7002df647', '2d8f4f20-4bd2-42ec-add4-30adbf8f9132');
INSERT INTO choices VALUES ('66d206be-d344-44d7-895e-f974376d95f1', now(), true, 'd24b2d12-dcac-4747-8d94-84b7002df647', 'bee674ed-4440-488d-b22f-1a00ac77952c');

-- INSERT INTO submissions VALUES ('22ea4b96-f132-45db-a5fd-30c53af2f79d', now(), 'c21589c4-86c6-4b0a-acb2-e0839c520f4e', 1, 1, 100, 'c4d129f9-41da-4a79-9f24-b9d79f1e86aa');
-- INSERT INTO submissions_choices VALUES ('22ea4b96-f132-45db-a5fd-30c53af2f79d', 'e096eef3-d427-4880-bea0-dbee4e304f81');
-- INSERT INTO submissions_choices VALUES ('22ea4b96-f132-45db-a5fd-30c53af2f79d', '515dbf1f-2372-4ec3-81a0-976b4567f356');
