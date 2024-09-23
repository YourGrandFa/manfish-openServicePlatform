/*
 Navicat Premium Data Transfer

 Source Server         : manfish
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : 127.0.0.1:3306
 Source Schema         : manfish_demo

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 24/09/2024 00:46:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `group_id` int(0) NOT NULL,
  `permission_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int(0) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 105 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add permission', 1, 'add_permission');
INSERT INTO `auth_permission` VALUES (2, 'Can change permission', 1, 'change_permission');
INSERT INTO `auth_permission` VALUES (3, 'Can delete permission', 1, 'delete_permission');
INSERT INTO `auth_permission` VALUES (4, 'Can view permission', 1, 'view_permission');
INSERT INTO `auth_permission` VALUES (5, 'Can add group', 2, 'add_group');
INSERT INTO `auth_permission` VALUES (6, 'Can change group', 2, 'change_group');
INSERT INTO `auth_permission` VALUES (7, 'Can delete group', 2, 'delete_group');
INSERT INTO `auth_permission` VALUES (8, 'Can view group', 2, 'view_group');
INSERT INTO `auth_permission` VALUES (9, 'Can add user', 3, 'add_user');
INSERT INTO `auth_permission` VALUES (10, 'Can change user', 3, 'change_user');
INSERT INTO `auth_permission` VALUES (11, 'Can delete user', 3, 'delete_user');
INSERT INTO `auth_permission` VALUES (12, 'Can view user', 3, 'view_user');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add auth group', 6, 'add_authgroup');
INSERT INTO `auth_permission` VALUES (22, 'Can change auth group', 6, 'change_authgroup');
INSERT INTO `auth_permission` VALUES (23, 'Can delete auth group', 6, 'delete_authgroup');
INSERT INTO `auth_permission` VALUES (24, 'Can view auth group', 6, 'view_authgroup');
INSERT INTO `auth_permission` VALUES (25, 'Can add auth group permissions', 7, 'add_authgrouppermissions');
INSERT INTO `auth_permission` VALUES (26, 'Can change auth group permissions', 7, 'change_authgrouppermissions');
INSERT INTO `auth_permission` VALUES (27, 'Can delete auth group permissions', 7, 'delete_authgrouppermissions');
INSERT INTO `auth_permission` VALUES (28, 'Can view auth group permissions', 7, 'view_authgrouppermissions');
INSERT INTO `auth_permission` VALUES (29, 'Can add auth permission', 8, 'add_authpermission');
INSERT INTO `auth_permission` VALUES (30, 'Can change auth permission', 8, 'change_authpermission');
INSERT INTO `auth_permission` VALUES (31, 'Can delete auth permission', 8, 'delete_authpermission');
INSERT INTO `auth_permission` VALUES (32, 'Can view auth permission', 8, 'view_authpermission');
INSERT INTO `auth_permission` VALUES (33, 'Can add auth user', 9, 'add_authuser');
INSERT INTO `auth_permission` VALUES (34, 'Can change auth user', 9, 'change_authuser');
INSERT INTO `auth_permission` VALUES (35, 'Can delete auth user', 9, 'delete_authuser');
INSERT INTO `auth_permission` VALUES (36, 'Can view auth user', 9, 'view_authuser');
INSERT INTO `auth_permission` VALUES (37, 'Can add auth user groups', 10, 'add_authusergroups');
INSERT INTO `auth_permission` VALUES (38, 'Can change auth user groups', 10, 'change_authusergroups');
INSERT INTO `auth_permission` VALUES (39, 'Can delete auth user groups', 10, 'delete_authusergroups');
INSERT INTO `auth_permission` VALUES (40, 'Can view auth user groups', 10, 'view_authusergroups');
INSERT INTO `auth_permission` VALUES (41, 'Can add auth user user permissions', 11, 'add_authuseruserpermissions');
INSERT INTO `auth_permission` VALUES (42, 'Can change auth user user permissions', 11, 'change_authuseruserpermissions');
INSERT INTO `auth_permission` VALUES (43, 'Can delete auth user user permissions', 11, 'delete_authuseruserpermissions');
INSERT INTO `auth_permission` VALUES (44, 'Can view auth user user permissions', 11, 'view_authuseruserpermissions');
INSERT INTO `auth_permission` VALUES (45, 'Can add django content type', 12, 'add_djangocontenttype');
INSERT INTO `auth_permission` VALUES (46, 'Can change django content type', 12, 'change_djangocontenttype');
INSERT INTO `auth_permission` VALUES (47, 'Can delete django content type', 12, 'delete_djangocontenttype');
INSERT INTO `auth_permission` VALUES (48, 'Can view django content type', 12, 'view_djangocontenttype');
INSERT INTO `auth_permission` VALUES (49, 'Can add django migrations', 13, 'add_djangomigrations');
INSERT INTO `auth_permission` VALUES (50, 'Can change django migrations', 13, 'change_djangomigrations');
INSERT INTO `auth_permission` VALUES (51, 'Can delete django migrations', 13, 'delete_djangomigrations');
INSERT INTO `auth_permission` VALUES (52, 'Can view django migrations', 13, 'view_djangomigrations');
INSERT INTO `auth_permission` VALUES (53, 'Can add django session', 14, 'add_djangosession');
INSERT INTO `auth_permission` VALUES (54, 'Can change django session', 14, 'change_djangosession');
INSERT INTO `auth_permission` VALUES (55, 'Can delete django session', 14, 'delete_djangosession');
INSERT INTO `auth_permission` VALUES (56, 'Can view django session', 14, 'view_djangosession');
INSERT INTO `auth_permission` VALUES (57, 'Can add tb dict', 15, 'add_tbdict');
INSERT INTO `auth_permission` VALUES (58, 'Can change tb dict', 15, 'change_tbdict');
INSERT INTO `auth_permission` VALUES (59, 'Can delete tb dict', 15, 'delete_tbdict');
INSERT INTO `auth_permission` VALUES (60, 'Can view tb dict', 15, 'view_tbdict');
INSERT INTO `auth_permission` VALUES (61, 'Can add tb file permission', 16, 'add_tbfilepermission');
INSERT INTO `auth_permission` VALUES (62, 'Can change tb file permission', 16, 'change_tbfilepermission');
INSERT INTO `auth_permission` VALUES (63, 'Can delete tb file permission', 16, 'delete_tbfilepermission');
INSERT INTO `auth_permission` VALUES (64, 'Can view tb file permission', 16, 'view_tbfilepermission');
INSERT INTO `auth_permission` VALUES (65, 'Can add tb file save', 17, 'add_tbfilesave');
INSERT INTO `auth_permission` VALUES (66, 'Can change tb file save', 17, 'change_tbfilesave');
INSERT INTO `auth_permission` VALUES (67, 'Can delete tb file save', 17, 'delete_tbfilesave');
INSERT INTO `auth_permission` VALUES (68, 'Can view tb file save', 17, 'view_tbfilesave');
INSERT INTO `auth_permission` VALUES (69, 'Can add tb service detail', 18, 'add_tbservicedetail');
INSERT INTO `auth_permission` VALUES (70, 'Can change tb service detail', 18, 'change_tbservicedetail');
INSERT INTO `auth_permission` VALUES (71, 'Can delete tb service detail', 18, 'delete_tbservicedetail');
INSERT INTO `auth_permission` VALUES (72, 'Can view tb service detail', 18, 'view_tbservicedetail');
INSERT INTO `auth_permission` VALUES (73, 'Can add tb service type', 19, 'add_tbservicetype');
INSERT INTO `auth_permission` VALUES (74, 'Can change tb service type', 19, 'change_tbservicetype');
INSERT INTO `auth_permission` VALUES (75, 'Can delete tb service type', 19, 'delete_tbservicetype');
INSERT INTO `auth_permission` VALUES (76, 'Can view tb service type', 19, 'view_tbservicetype');
INSERT INTO `auth_permission` VALUES (77, 'Can add tb task order', 20, 'add_tbtaskorder');
INSERT INTO `auth_permission` VALUES (78, 'Can change tb task order', 20, 'change_tbtaskorder');
INSERT INTO `auth_permission` VALUES (79, 'Can delete tb task order', 20, 'delete_tbtaskorder');
INSERT INTO `auth_permission` VALUES (80, 'Can view tb task order', 20, 'view_tbtaskorder');
INSERT INTO `auth_permission` VALUES (81, 'Can add tb task process', 21, 'add_tbtaskprocess');
INSERT INTO `auth_permission` VALUES (82, 'Can change tb task process', 21, 'change_tbtaskprocess');
INSERT INTO `auth_permission` VALUES (83, 'Can delete tb task process', 21, 'delete_tbtaskprocess');
INSERT INTO `auth_permission` VALUES (84, 'Can view tb task process', 21, 'view_tbtaskprocess');
INSERT INTO `auth_permission` VALUES (85, 'Can add tm account', 22, 'add_tmaccount');
INSERT INTO `auth_permission` VALUES (86, 'Can change tm account', 22, 'change_tmaccount');
INSERT INTO `auth_permission` VALUES (87, 'Can delete tm account', 22, 'delete_tmaccount');
INSERT INTO `auth_permission` VALUES (88, 'Can view tm account', 22, 'view_tmaccount');
INSERT INTO `auth_permission` VALUES (89, 'Can add tm account log', 23, 'add_tmaccountlog');
INSERT INTO `auth_permission` VALUES (90, 'Can change tm account log', 23, 'change_tmaccountlog');
INSERT INTO `auth_permission` VALUES (91, 'Can delete tm account log', 23, 'delete_tmaccountlog');
INSERT INTO `auth_permission` VALUES (92, 'Can view tm account log', 23, 'view_tmaccountlog');
INSERT INTO `auth_permission` VALUES (93, 'Can add tm license', 24, 'add_tmlicense');
INSERT INTO `auth_permission` VALUES (94, 'Can change tm license', 24, 'change_tmlicense');
INSERT INTO `auth_permission` VALUES (95, 'Can delete tm license', 24, 'delete_tmlicense');
INSERT INTO `auth_permission` VALUES (96, 'Can view tm license', 24, 'view_tmlicense');
INSERT INTO `auth_permission` VALUES (97, 'Can add tp user', 25, 'add_tpuser');
INSERT INTO `auth_permission` VALUES (98, 'Can change tp user', 25, 'change_tpuser');
INSERT INTO `auth_permission` VALUES (99, 'Can delete tp user', 25, 'delete_tpuser');
INSERT INTO `auth_permission` VALUES (100, 'Can view tp user', 25, 'view_tpuser');
INSERT INTO `auth_permission` VALUES (101, 'Can add tp user log', 26, 'add_tpuserlog');
INSERT INTO `auth_permission` VALUES (102, 'Can change tp user log', 26, 'change_tpuserlog');
INSERT INTO `auth_permission` VALUES (103, 'Can delete tp user log', 26, 'delete_tpuserlog');
INSERT INTO `auth_permission` VALUES (104, 'Can view tp user log', 26, 'view_tpuserlog');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$600000$dBH7dFK7TYQOa6xSNqncL3$QNzpajJUoOU55C23GUWRIirPiIS7r4cmqwI6RYWqkdk=', NULL, 0, 'test', '', '', 'xxx@qq.com', 0, 1, '2024-09-24 00:05:38.733806');
INSERT INTO `auth_user` VALUES (2, 'pbkdf2_sha256$600000$ovSBfigfI5lnjDiRdbZxD6$mQgOrHn2Bqv6ed/vZK2lbndu5QHyAu8JURQOrl1fpak=', '2024-09-24 00:08:58.669914', 0, 'dhl', '', '', 'xxx@qq.com', 0, 1, '2024-09-24 00:06:18.016879');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` int(0) NOT NULL,
  `group_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` int(0) NOT NULL,
  `permission_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (2, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (1, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'manfish_AI_Service', 'authgroup');
INSERT INTO `django_content_type` VALUES (7, 'manfish_AI_Service', 'authgrouppermissions');
INSERT INTO `django_content_type` VALUES (8, 'manfish_AI_Service', 'authpermission');
INSERT INTO `django_content_type` VALUES (9, 'manfish_AI_Service', 'authuser');
INSERT INTO `django_content_type` VALUES (10, 'manfish_AI_Service', 'authusergroups');
INSERT INTO `django_content_type` VALUES (11, 'manfish_AI_Service', 'authuseruserpermissions');
INSERT INTO `django_content_type` VALUES (12, 'manfish_AI_Service', 'djangocontenttype');
INSERT INTO `django_content_type` VALUES (13, 'manfish_AI_Service', 'djangomigrations');
INSERT INTO `django_content_type` VALUES (14, 'manfish_AI_Service', 'djangosession');
INSERT INTO `django_content_type` VALUES (15, 'manfish_AI_Service', 'tbdict');
INSERT INTO `django_content_type` VALUES (16, 'manfish_AI_Service', 'tbfilepermission');
INSERT INTO `django_content_type` VALUES (17, 'manfish_AI_Service', 'tbfilesave');
INSERT INTO `django_content_type` VALUES (18, 'manfish_AI_Service', 'tbservicedetail');
INSERT INTO `django_content_type` VALUES (19, 'manfish_AI_Service', 'tbservicetype');
INSERT INTO `django_content_type` VALUES (20, 'manfish_AI_Service', 'tbtaskorder');
INSERT INTO `django_content_type` VALUES (21, 'manfish_AI_Service', 'tbtaskprocess');
INSERT INTO `django_content_type` VALUES (22, 'manfish_AI_Service', 'tmaccount');
INSERT INTO `django_content_type` VALUES (23, 'manfish_AI_Service', 'tmaccountlog');
INSERT INTO `django_content_type` VALUES (24, 'manfish_AI_Service', 'tmlicense');
INSERT INTO `django_content_type` VALUES (25, 'manfish_AI_Service', 'tpuser');
INSERT INTO `django_content_type` VALUES (26, 'manfish_AI_Service', 'tpuserlog');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'sessions', '0001_initial', '2024-09-24 00:04:35.783239');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0001_initial', '2024-09-24 00:04:40.849235');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2024-09-24 00:04:42.489463');
INSERT INTO `django_migrations` VALUES (4, 'contenttypes', '0002_remove_content_type_name', '2024-09-24 00:04:42.797772');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0002_alter_permission_name_max_length', '2024-09-24 00:04:42.984974');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0003_alter_user_email_max_length', '2024-09-24 00:04:43.100603');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0004_alter_user_username_opts', '2024-09-24 00:04:43.170602');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0005_alter_user_last_login_null', '2024-09-24 00:04:43.335776');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0006_require_contenttypes_0002', '2024-09-24 00:04:43.402602');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0007_alter_validators_add_error_messages', '2024-09-24 00:04:43.472601');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0008_alter_user_username_max_length', '2024-09-24 00:04:43.650907');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0009_alter_user_last_name_max_length', '2024-09-24 00:04:43.833371');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0010_alter_group_name_max_length', '2024-09-24 00:04:43.962570');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0011_update_proxy_permissions', '2024-09-24 00:04:44.133045');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0012_alter_user_first_name_max_length', '2024-09-24 00:04:44.318084');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('dkzivi6oxipa3thtdbff9t7okqxc9cwc', '.eJxVjEEOwiAUBe_C2hD4gKUu3XsGArxfqRqalHZlvLsh6UK3b2beW4S4byXsjdcwQ1wEidPvlmJ-cu0Aj1jvi8xL3dY5ya7IgzZ5W8Cv6-H-HZTYSq8pengMzBOxdjA5wUD7rEBgy9r46JSftDrTmLQzTBmZRiQM1nojPl8OyTiJ:1sslcQ:s7Ajy9UvdOlCzLy1on1KT6mQaue2vC5KtxGFmxrriP4', '2024-09-25 00:08:58.708036');

-- ----------------------------
-- Table structure for tb_dict
-- ----------------------------
DROP TABLE IF EXISTS `tb_dict`;
CREATE TABLE `tb_dict`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `dict_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '服务器或区域、其他描述',
  `dict_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典id、名称、代指词',
  `dict_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '目标值',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 82 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_dict
-- ----------------------------
INSERT INTO `tb_dict` VALUES (60, 'welcome_url', '/person/permission', '用户授权', '2024-09-09 11:00:49');
INSERT INTO `tb_dict` VALUES (61, 'welcome_url', '/service/home', '服务列表', '2024-09-09 11:00:49');
INSERT INTO `tb_dict` VALUES (62, 'welcome_url', '/order/list', '订单进度', '2024-09-09 11:00:49');
INSERT INTO `tb_dict` VALUES (63, 'license_state', '0', '未开启', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (64, 'license_state', '1', '待使用', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (65, 'license_state', '2', '已使用', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (66, 'license_state', '3', '已删除', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (67, 'user_type', '0', '服务商', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (68, 'user_type', '1', '客户', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (69, 'user_state', '0', '未启用', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (70, 'user_state', '1', '正常使用', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (71, 'user_state', '2', '封禁', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (72, 'account_state', '0', '未启用', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (73, 'account_state', '1', '正常使用', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (74, 'account_state', '2', '冻结', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (75, 'account_state', '3', '封禁', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (76, 'order_state', '0', '未执行', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (77, 'order_state', '1', '正在执行', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (78, 'order_state', '2', '执行完成', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (79, 'order_state', '3', '执行失败', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (80, 'process_state', '1', '执行成功', '2024-09-10 10:37:22');
INSERT INTO `tb_dict` VALUES (81, 'process_state', '2', '执行失败', '2024-09-10 10:37:22');

-- ----------------------------
-- Table structure for tb_file_permission
-- ----------------------------
DROP TABLE IF EXISTS `tb_file_permission`;
CREATE TABLE `tb_file_permission`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `file_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件编号',
  `user_id` int(0) NULL DEFAULT NULL COMMENT '用户编号',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 128 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_file_permission
-- ----------------------------

-- ----------------------------
-- Table structure for tb_file_save
-- ----------------------------
DROP TABLE IF EXISTS `tb_file_save`;
CREATE TABLE `tb_file_save`  (
  `file_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件id',
  `file_belong` int(0) NULL DEFAULT NULL COMMENT '文件归属者user_id',
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名称',
  `local_save_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '本地存储地址',
  `oss_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '阿里云oss存储地址',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `state` int(0) NULL DEFAULT NULL COMMENT '当前状态，0为禁止访问，1为允许访问',
  PRIMARY KEY (`file_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_file_save
-- ----------------------------

-- ----------------------------
-- Table structure for tb_service_detail
-- ----------------------------
DROP TABLE IF EXISTS `tb_service_detail`;
CREATE TABLE `tb_service_detail`  (
  `service_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '服务id',
  `user_id` int(0) NULL DEFAULT NULL COMMENT '服务者/执行者user_id',
  `type_no` int(0) NULL DEFAULT NULL COMMENT '任务类型编号',
  `online_state` int(0) NULL DEFAULT NULL COMMENT '服务上线状态，0离线，1在线',
  `state` int(0) NULL DEFAULT NULL COMMENT '服务状态，0未部署，1已部署，2已下架，3已清除，4正在维护',
  PRIMARY KEY (`service_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '服务资源清单' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_service_detail
-- ----------------------------
INSERT INTO `tb_service_detail` VALUES (1, 4, 1, 0, 1);
INSERT INTO `tb_service_detail` VALUES (2, 4, 2, 0, 1);
INSERT INTO `tb_service_detail` VALUES (3, 4, 3, 0, 1);
INSERT INTO `tb_service_detail` VALUES (4, 4, 4, 0, 1);
INSERT INTO `tb_service_detail` VALUES (5, 4, 5, 0, 1);
INSERT INTO `tb_service_detail` VALUES (8, 4, 6, 0, 1);
INSERT INTO `tb_service_detail` VALUES (9, 4, 7, 0, 1);
INSERT INTO `tb_service_detail` VALUES (10, 4, 8, 0, 1);

-- ----------------------------
-- Table structure for tb_service_type
-- ----------------------------
DROP TABLE IF EXISTS `tb_service_type`;
CREATE TABLE `tb_service_type`  (
  `type_no` int(0) NOT NULL AUTO_INCREMENT COMMENT '服务编号',
  `service_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '服务名称',
  `service_desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '服务简介',
  `price` decimal(8, 2) NULL DEFAULT NULL COMMENT '使用单价：元/次',
  `service_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '管理服务器地址',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `state` int(0) NULL DEFAULT NULL COMMENT '管理服务器状态，0表示离线，1表示在线，2表示停用',
  PRIMARY KEY (`type_no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_service_type
-- ----------------------------
INSERT INTO `tb_service_type` VALUES (1, 'MP4转MP3', 'MP4转MP3', 1.00, NULL, '2024-08-23 16:36:03', 1);
INSERT INTO `tb_service_type` VALUES (2, '人物抠图', '人物抠图', 1.50, NULL, '2024-08-23 16:36:03', 1);
INSERT INTO `tb_service_type` VALUES (3, '替换证件照背景色', '替换证件照背景色', 2.00, NULL, '2024-08-23 16:36:03', 1);
INSERT INTO `tb_service_type` VALUES (4, 'GIF制作', 'GIF制作', 0.50, NULL, '2024-08-23 16:38:30', 1);
INSERT INTO `tb_service_type` VALUES (5, '渐变GIF制作', '渐变GIF制作', 1.00, NULL, '2024-08-23 16:38:30', 1);
INSERT INTO `tb_service_type` VALUES (6, 'SD图片生成', 'SD图片生成', 2.00, NULL, '2024-09-05 15:54:43', 1);
INSERT INTO `tb_service_type` VALUES (7, '歌曲翻唱', 'so-vits', 5.00, NULL, '2024-09-05 15:56:13', 1);
INSERT INTO `tb_service_type` VALUES (8, '语音克隆', 'GPT-sovits', 1.50, NULL, '2024-09-05 15:56:15', 1);

-- ----------------------------
-- Table structure for tb_task_order
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_order`;
CREATE TABLE `tb_task_order`  (
  `order_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '任务自增id',
  `type_no` int(0) NULL DEFAULT NULL COMMENT '任务类型编号',
  `link_id` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '下级扩展任务id，当state为3时有值',
  `desc_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '文字要求',
  `desc_appendix` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '输入附件，file_id，多个附件以|分开',
  `applyer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '申请者',
  `apply_time` datetime(0) NULL DEFAULT NULL COMMENT '申请时间',
  `spend_money` decimal(8, 2) NULL DEFAULT NULL COMMENT '本次花费金额',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `performer` int(0) NULL DEFAULT NULL COMMENT '分配执行者',
  `allocate_time` datetime(0) NULL DEFAULT NULL COMMENT '分配时间',
  `finish_time` datetime(0) NULL DEFAULT NULL COMMENT '结束时间',
  `state` int(0) NULL DEFAULT NULL COMMENT '执行状态，0为未执行，1为正在执行，2为执行完成，3为执行失败',
  PRIMARY KEY (`order_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '任务订单' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_task_order
-- ----------------------------

-- ----------------------------
-- Table structure for tb_task_process
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_process`;
CREATE TABLE `tb_task_process`  (
  `process_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '流程自增id',
  `performer` int(0) NULL DEFAULT NULL COMMENT '执行者',
  `order_id` int(0) NULL DEFAULT NULL COMMENT '关联订单id',
  `start_time` datetime(0) NULL DEFAULT NULL COMMENT '开始执行时间/接单时间',
  `end_time` datetime(0) NULL DEFAULT NULL COMMENT '结束时间',
  `result` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '执行结果',
  `appendix` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '结果附件，一般为file_id，若多个以|分割',
  `state` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '执行状态，1为执行成功，2为执行失败',
  PRIMARY KEY (`process_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '任务执行进度' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_task_process
-- ----------------------------

-- ----------------------------
-- Table structure for tm_account
-- ----------------------------
DROP TABLE IF EXISTS `tm_account`;
CREATE TABLE `tm_account`  (
  `account_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '账户id',
  `account_money` decimal(8, 2) NULL DEFAULT NULL COMMENT '账户余额',
  `lock_money` decimal(8, 2) NULL DEFAULT NULL COMMENT '锁定金额',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `state` int(0) NULL DEFAULT NULL COMMENT '账户状态，0为未启用，1为启用，2为冻结，3为封禁',
  PRIMARY KEY (`account_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tm_account
-- ----------------------------
INSERT INTO `tm_account` VALUES ('5ead6178-b950-4f29-8099-e43dbf757910', 0.00, 0.00, '2024-09-05 10:56:02', NULL, 1);
INSERT INTO `tm_account` VALUES ('6e39bfdb-6630-44b8-811a-bae872b2941a', 0.00, 0.00, '2024-09-05 10:54:55', NULL, 1);
INSERT INTO `tm_account` VALUES ('cca05c77-c432-4788-b422-02a0a945f5b8', 0.00, 0.00, '2024-09-13 22:02:52', NULL, 1);

-- ----------------------------
-- Table structure for tm_account_log
-- ----------------------------
DROP TABLE IF EXISTS `tm_account_log`;
CREATE TABLE `tm_account_log`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `order_effect_ret` int(0) NULL DEFAULT NULL COMMENT '是否是订单影响，0否，1是',
  `order_id` int(0) NULL DEFAULT NULL COMMENT '关联订单编号，order_effect_ret为否是为空',
  `reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '金额变动发生原因',
  `account_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '影响的账户id',
  `effect` decimal(8, 2) NULL DEFAULT NULL COMMENT '金额影响',
  `before` decimal(8, 2) NULL DEFAULT NULL COMMENT '变动之前的金额',
  `after` decimal(8, 2) NULL DEFAULT NULL COMMENT '变动之后的金额',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 51 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tm_account_log
-- ----------------------------

-- ----------------------------
-- Table structure for tm_license
-- ----------------------------
DROP TABLE IF EXISTS `tm_license`;
CREATE TABLE `tm_license`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `license_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '授权码',
  `save_money` decimal(8, 2) NULL DEFAULT NULL COMMENT '价值：元',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `use_time` datetime(0) NULL DEFAULT NULL COMMENT '使用时间',
  `state` int(0) NULL DEFAULT NULL COMMENT '当前状态，0为未开启，1为待用，2为已使用，3为删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `only_license`(`license_code`) USING BTREE COMMENT '唯一授权码'
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tm_license
-- ----------------------------
INSERT INTO `tm_license` VALUES (1, 'df9afa81-79af-4efb-b5f0-d60ab44bd988', 100.00, '2024-09-10 11:21:59', NULL, 2);
INSERT INTO `tm_license` VALUES (2, 'b5bb2682-d281-4488-bcab-ec0caebdbdce', 100.00, '2024-09-17 16:20:29', NULL, 2);

-- ----------------------------
-- Table structure for tp_user
-- ----------------------------
DROP TABLE IF EXISTS `tp_user`;
CREATE TABLE `tp_user`  (
  `user_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `user_type` int(0) NULL DEFAULT NULL COMMENT '用户类型，0为服务商，1为客户',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '授权码',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `all_done` int(0) NULL DEFAULT NULL COMMENT '总处理单量，只有服务商会有相关参数',
  `success_done` int(0) NULL DEFAULT NULL COMMENT '完成单',
  `bad_done` int(0) NULL DEFAULT NULL COMMENT '失败单',
  `account_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '账户编码',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `state` int(0) NULL DEFAULT NULL COMMENT '当前状态，0为未启用，1为正常使用，2为封禁',
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `only_username`(`username`) USING BTREE COMMENT '唯一用户名'
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tp_user
-- ----------------------------
INSERT INTO `tp_user` VALUES (3, 1, 'test', 'JtqhPMISpqijpnOw', 'XiG16VTU', NULL, NULL, NULL, '6e39bfdb-6630-44b8-811a-bae872b2941a', '2024-09-05 10:54:54', 1);
INSERT INTO `tp_user` VALUES (4, 0, 'manfish', '4rcVfCMiTEAFQodC', '3xzpnse0', 10, 10, 0, '5ead6178-b950-4f29-8099-e43dbf757910', '2024-09-05 10:56:02', 1);
INSERT INTO `tp_user` VALUES (5, 1, 'dhl', 'Hf0jFL3JrnD2pt6Z', 'KveJr4mI', NULL, NULL, NULL, 'cca05c77-c432-4788-b422-02a0a945f5b8', '2024-09-13 22:02:52', 1);

-- ----------------------------
-- Table structure for tp_user_log
-- ----------------------------
DROP TABLE IF EXISTS `tp_user_log`;
CREATE TABLE `tp_user_log`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `user_id` int(0) NULL DEFAULT NULL COMMENT '服务商用户编号',
  `cmd` int(0) NULL DEFAULT NULL COMMENT '行动代码',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10717 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tp_user_log
-- ----------------------------
INSERT INTO `tp_user_log` VALUES (10717, 4, 0, '2024-09-24 00:23:14');
INSERT INTO `tp_user_log` VALUES (10718, 4, 0, '2024-09-24 00:23:24');
INSERT INTO `tp_user_log` VALUES (10719, 4, 0, '2024-09-24 00:23:34');
INSERT INTO `tp_user_log` VALUES (10720, 4, 0, '2024-09-24 00:23:44');
INSERT INTO `tp_user_log` VALUES (10721, 4, 0, '2024-09-24 00:23:54');
INSERT INTO `tp_user_log` VALUES (10722, 4, 0, '2024-09-24 00:24:04');
INSERT INTO `tp_user_log` VALUES (10723, 4, 0, '2024-09-24 00:24:14');
INSERT INTO `tp_user_log` VALUES (10724, 4, 0, '2024-09-24 00:24:24');
INSERT INTO `tp_user_log` VALUES (10725, 4, 0, '2024-09-24 00:24:34');
INSERT INTO `tp_user_log` VALUES (10726, 4, 0, '2024-09-24 00:24:44');
INSERT INTO `tp_user_log` VALUES (10727, 4, 0, '2024-09-24 00:24:54');
INSERT INTO `tp_user_log` VALUES (10728, 4, 0, '2024-09-24 00:26:26');
INSERT INTO `tp_user_log` VALUES (10729, 4, 0, '2024-09-24 00:29:32');
INSERT INTO `tp_user_log` VALUES (10730, 4, 0, '2024-09-24 00:29:42');

SET FOREIGN_KEY_CHECKS = 1;
