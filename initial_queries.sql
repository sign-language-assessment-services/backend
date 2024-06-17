INSERT INTO assessments VALUES ('c4d129f9-41da-4a79-9f24-b9d79f1e86aa', now(), 'Test Assessment');
INSERT INTO multimedia_files VALUES ('770ff2c3-3197-4096-9eeb-040b6d6e7532', now(), 'slportal', 'foobar');
INSERT INTO multimedia_files VALUES ('49a412fe-e513-4d77-a6a8-841ab0676105', now(), 'slportal', 'barfoo');
INSERT INTO exercises VALUES ('878889dd-199a-44e8-b111-7a4446844dbd', now(), 1, 'c4d129f9-41da-4a79-9f24-b9d79f1e86aa', '770ff2c3-3197-4096-9eeb-040b6d6e7532');
INSERT INTO choices VALUES ('e096eef3-d427-4880-bea0-dbee4e304f81', now(), true, '878889dd-199a-44e8-b111-7a4446844dbd', '770ff2c3-3197-4096-9eeb-040b6d6e7532');
INSERT INTO choices VALUES ('515dbf1f-2372-4ec3-81a0-976b4567f356', now(), false, '878889dd-199a-44e8-b111-7a4446844dbd', '770ff2c3-3197-4096-9eeb-040b6d6e7532');
INSERT INTO submissions VALUES ('22ea4b96-f132-45db-a5fd-30c53af2f79d', now(), 'c21589c4-86c6-4b0a-acb2-e0839c520f4e', 1, 1, 100, 'c4d129f9-41da-4a79-9f24-b9d79f1e86aa');
INSERT INTO submissions_choices VALUES ('22ea4b96-f132-45db-a5fd-30c53af2f79d', 'e096eef3-d427-4880-bea0-dbee4e304f81');
INSERT INTO submissions_choices VALUES ('22ea4b96-f132-45db-a5fd-30c53af2f79d', '515dbf1f-2372-4ec3-81a0-976b4567f356');
