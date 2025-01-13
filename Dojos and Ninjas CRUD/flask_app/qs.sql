INSERT INTO `dojos` (`name`, `created_at`, `updated_at`) VALUES
('Prealpha', NOW(), NOW()),
('Alpha', NOW(), NOW()),
('Beta', NOW(), NOW());

DELETE FROM `dojos` WHERE `name` IN ('Prealpha', 'Alpha', 'Beta');

INSERT INTO `dojos` (`name`, `created_at`, `updated_at`) VALUES
('Jon', NOW(), NOW()),
('Jane', NOW(), NOW()),
('Jet', NOW(), NOW());


INSERT INTO `ninjas` (`first_name`, `last_name`, `age`, `dojos_id`, `created_at`, `updated_at`) VALUES
('Fon', 'Prelpha', 21, 1, NOW(), NOW()),
('Fane', 'Prelpha', 22, 1, NOW(), NOW()),
('Fet', 'Prealpha', 23, 1, NOW(), NOW());

INSERT INTO `ninjas` (`first_name`, `last_name`, `age`, `dojos_id`, `created_at`, `updated_at`) VALUES
('Son', 'Alpha', 24, 2, NOW(), NOW()),
('Sane', 'Alpha', 25, 2, NOW(), NOW()),
('Set', 'Alpha', 26, 2, NOW(), NOW());

INSERT INTO `ninjas` (`first_name`, `last_name`, `age`, `dojos_id`, `created_at`, `updated_at`) VALUES
('Von', 'Beta', 27, 3, NOW(), NOW()),
('Vane', 'Beta', 28, 3, NOW(), NOW()),
('Vet', 'Beta', 29, 3, NOW(), NOW());

SELECT * FROM `ninjas` WHERE `dojos_id` = 1;

SELECT * FROM `ninjas` WHERE `dojos_id` = 3;

SELECT `dojos`.* FROM `dojos`
JOIN `ninjas` ON `dojos`.`id` = `ninjas`.`dojos_id`
WHERE `ninjas`.`id` = (SELECT MAX(`id`) FROM `ninjas`);

SELECT `ninjas`.*, `dojos`.* FROM `ninjas`
JOIN `dojos` ON `ninjas`.`dojos_id` = `dojos`.`id`
WHERE `ninjas`.`id` = 6;


SELECT `ninjas`.*, `dojos`.* FROM `ninjas`
JOIN `dojos` ON `ninjas`.`dojos_id` = `dojos`.`id`;















