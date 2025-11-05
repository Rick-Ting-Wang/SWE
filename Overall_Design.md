# Komodo Hub Overall Design

**author**: Rick Ting Wang(14553505)


## 用户类型与功能

### 1. **系统管理员 (Superuser)**
**代表人物:** Asnawi (Yayasan Komodo 账户开发人员)

**功能:**
- 管理整体系统运营
- 注册学校和社区
- 管理组织账户
- 通过电子邮件与订阅者互动
- 生成业务仪表板
- 监控系统范围内的活动

**数据库映射:**
- `users` 表 (user_type = 'admin')
- `organizations` 表 (注册管理)
- `business_analytics` 表 (仪表板数据)
- `access_logs` 表 (监控活动)

---

### 2. **项目总监/管理层**
**代表人物:** Tegar Prayudi

**功能:**
- 访问业务分析仪表板
- 检索订阅数据
- 监控用户行为和人口统计
- 跟踪服务可用性和受欢迎程度
- 基于数据做出战略决策

**数据库映射:**
- `users` 表 (管理权限)
- `business_analytics` 表 (分析数据)
- `organizations` 表 (订阅统计)
- `access_logs` 表 (用户行为数据)

---

### 3. **校长**
**代表人物:** Khairunnisa

**功能:**
- 订阅计划
- 管理学校资料
- 监督教师和学生注册
- 生成并分发学生唯一访问码
- 控制隐私设置（公开与内部）
- 访问教师和学生的高级数据
- 管理学校图书馆可见性

**数据库映射:**
- `users` 表 (user_type = 'principal')
- `organizations` 表 (学校资料、订阅状态)
- `organization_members` 表 (生成访问码)
- `content_library` 表 (管理图书馆可见性)

---

### 4. **学校管理员**
**代表人物:** Ayu Lestari

**功能:**
- 处理订阅管理
- 处理账户注册
- 管理学生入学
- 执行校长授权的管理任务

**数据库映射:**
- `users` 表 (user_type = 'school_admin')
- `organizations` 表 (订阅管理)
- `organization_members` 表 (注册和入学)

---

### 5. **教师**
**代表人物:** Bintang Akbar

**功能:**
- 管理分配的班级
- 开发和发布课程大纲
- 创建和管理内容/活动
- 接纳学生进入班级
- 评估学生进度
- 生成学生进度报告
- 向学生发送电子邮件
- 向学生发送直接消息
- 在学生作品/提交上留下笔记
- 查看学生活动和贡献
- 访问 Komodo Hub 图书馆的学习材料

**数据库映射:**
- `users` 表 (user_type = 'teacher')
- `classes` 表 (班级管理)
- `class_enrollments` 表 (学生入学)
- `activities` 表 (创建活动)
- `assessments` 表 (评估)
- `messages` 表 (直接消息)
- `notes` 表 (留下笔记)
- `content_library` 表 (访问材料)

---

### 6. **学生**

**功能:**
- 个性化账户（头像、配色方案）
- 查看已注册项目
- 访问学习材料
- 参与活动（课堂内和户外）
- 提交作业和报告
- 报告濒危物种目击
- 分享内容
- 给教师发消息
- 回复教师笔记
- 上传作品到学校图书馆
- 创建创意画布（作品集）

**数据库映射:**
- `users` 表 (user_type = 'student')
- `user_profiles` 表 (个性化，is_public = false)
- `organization_members` 表 (访问码)
- `class_enrollments` 表 (班级注册)
- `program_enrollments` 表 (项目注册)
- `submissions` 表 (作业提交)
- `species_sightings` 表 (目击报告)
- `content_library` 表 (上传作品)
- `creative_canvas` 表 (作品集)
- `messages` 表 (与教师通信)

---

### 7. **社区主席**
**代表人物:** Besoeki Rachmat

**功能:**
- 订阅社区到计划
- 注册社区成员
- 管理社区资料和图书馆
- 贡献文章、散文、专栏
- 报告物种目击
- 查看成员贡献

**数据库映射:**
- `users` 表 (user_type = 'community_chair')
- `organizations` 表 (org_type = 'community')
- `organization_members` 表 (成员注册)
- `content_library` 表 (贡献内容，is_public = true)
- `species_sightings` 表 (目击报告)

---

### 8. **社区成员**

**功能:**
- 创建和管理资料（公开可见）
- 为保护项目做出贡献
- 提交文章和报告
- 报告物种目击
- 分享内容到社区图书馆

**数据库映射:**
- `users` 表 (user_type = 'community_member')
- `user_profiles` 表 (is_public = true)
- `organization_members` 表 (社区关联)
- `content_library` 表 (贡献，is_public = true)
- `species_sightings` 表 (报告)

---

### 9. **安全合规官**
**代表人物:** Bhaskara

**功能:**
- 监控安全合规性
- 审计系统安全措施
- 确保数据保护标准
- 评估认证和访问控制

**数据库映射:**
- `users` 表 (高级权限)
- `access_logs` 表 (审计追踪)
- 所有表（审计权限）

---

### 10. **普通公众（未注册用户）**

**功能:**
- 浏览 Komodo Hub 知识库
- 查看社区图书馆和成员资料
- 查看学校图书馆（但不能查看学生资料）
- 访问有关濒危物种的教育内容

**数据库映射:**
- `content_library` 表 (is_public = true)
- `user_profiles` 表 (仅社区成员，is_public = true)
- `organizations` 表 (仅 is_public = true)

---

## 数据库设计

### **核心表结构**

#### **1. Users 表 - 用户**
```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_image ENUM('1','2','3','4','5','6','7','8','9'),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type ENUM('admin', 'principal', 'school_admin', 'teacher', 
                   'student', 'community_chair', 'community_member', 'public') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_user_type (user_type),
    INDEX idx_email (email)
);
```

**用途:** 
- 所有用户类型的核心表
- 认证和授权
- 用户类型区分

---

#### **2. Organizations 表 - 组织**
```sql
CREATE TABLE organizations (
    org_id INT PRIMARY KEY AUTO_INCREMENT,
    org_type ENUM('school', 'community') NOT NULL,
    org_name VARCHAR(200) NOT NULL,
    org_profile TEXT,
    is_public BOOLEAN DEFAULT TRUE,
    subscription_status ENUM('active', 'inactive', 'pending') DEFAULT 'pending',
    subscription_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_org_type (org_type),
    INDEX idx_subscription_status (subscription_status)
);
```

**用途:**
- 校长管理学校资料
- 社区主席管理社区资料
- 订阅管理
- 隐私控制（学校 vs 社区）

---

#### **3. Organization_Members 表 - 组织成员**
```sql
CREATE TABLE organization_members (
    membership_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT NOT NULL,
    user_id INT NOT NULL,
    role ENUM('principal', 'admin', 'teacher', 'student', 'chairman', 'member') NOT NULL,
    access_code VARCHAR(50) UNIQUE,  -- 仅用于学生
    joined_date DATE NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_org_user (org_id, user_id),
    INDEX idx_role (role)
);
```

**用途:**
- 将用户链接到组织
- 角色管理
- 学生访问码生成和验证
- 权限控制

---

#### **4. Classes 表 - 班级**
```sql
CREATE TABLE classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT NOT NULL,
    teacher_id INT NOT NULL,
    class_name VARCHAR(100) NOT NULL,
    syllabus TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_teacher (teacher_id)
);
```

**用途:**
- 教师创建和管理班级
- 课程大纲管理
- 班级组织

---

#### **5. Class_Enrollments 表 - 班级入学**
```sql
CREATE TABLE class_enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    class_id INT NOT NULL,
    student_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_class_student (class_id, student_id),
    INDEX idx_student (student_id)
);
```

**用途:**
- 教师将学生接纳进班级
- 学生查看已注册班级
- 访问控制（仅分配的教师可查看学生数据）

---

#### **6. Programs 表 - 保护项目**
```sql
CREATE TABLE programs (
    program_id INT PRIMARY KEY AUTO_INCREMENT,
    program_name VARCHAR(200) NOT NULL,
    description TEXT,
    program_type ENUM('internal', 'local', 'regional', 'national') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_program_type (program_type)
);
```

**用途:**
- Komodo Hub 提供的保护项目
- 项目分类
- 教师和学生选择参与的项目

---

#### **7. Program_Enrollments 表 - 项目注册**
```sql
CREATE TABLE program_enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    program_id INT NOT NULL,
    user_id INT,  -- 个人用户
    org_id INT,   -- 或组织
    enrollment_date DATE NOT NULL,
    status ENUM('active', 'completed', 'dropped') DEFAULT 'active',
    FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
    CHECK (user_id IS NOT NULL OR org_id IS NOT NULL),
    INDEX idx_program (program_id),
    INDEX idx_user (user_id),
    INDEX idx_org (org_id)
);
```

**用途:**
- 学生查看已注册项目
- 组织（学校/社区）项目参与
- 项目跟踪

---

#### **8. Activities 表 - 活动**
```sql
CREATE TABLE activities (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    program_id INT NOT NULL,
    class_id INT,  -- 教师创建的特定班级活动
    activity_name VARCHAR(200) NOT NULL,
    activity_type ENUM('in-class', 'outdoor', 'challenge', 'game', 'assessment') NOT NULL,
    description TEXT,
    created_by INT NOT NULL,  -- 创建者（教师或管理员）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_program (program_id),
    INDEX idx_class (class_id)
);
```

**用途:**
- 教师创建课堂和户外活动
- 学生查找和执行活动
- 活动管理

---

#### **9. Content_Library 表 - 内容库**
```sql
CREATE TABLE content_library (
    content_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(300) NOT NULL,
    content_type ENUM('article', 'essay', 'report', 'sighting', 'photo', 
                     'video', 'educational_material') NOT NULL,
    content_data TEXT,  -- 文本内容或文件路径
    created_by INT NOT NULL,
    org_id INT,  -- 组织图书馆
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
    INDEX idx_content_type (content_type),
    INDEX idx_org (org_id),
    INDEX idx_public (is_public)
);
```

**用途:**
- 学生上传作品到学校图书馆
- 社区成员贡献文章
- 教师访问学习材料
- 公众浏览知识库
- 隐私控制（学校 is_public = false for students, true for library）

---

#### **10. Species_Sightings 表 - 物种目击**
```sql
CREATE TABLE species_sightings (
    sighting_id INT PRIMARY KEY AUTO_INCREMENT,
    species_name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    date_time DATETIME NOT NULL,
    description TEXT,
    photo_path VARCHAR(500),
    reported_by INT NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reported_by) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_species (species_name),
    INDEX idx_reporter (reported_by),
    INDEX idx_verified (verified)
);
```

**用途:**
- 学生报告濒危物种目击
- 社区成员贡献目击数据
- 教师在目击上留下笔记
- 保护数据收集

---

#### **11. Submissions 表 - 作业提交**
```sql
CREATE TABLE submissions (
    submission_id INT PRIMARY KEY AUTO_INCREMENT,
    activity_id INT NOT NULL,
    student_id INT NOT NULL,
    submission_data TEXT,
    submission_file_path VARCHAR(500),
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('submitted', 'graded', 'returned') DEFAULT 'submitted',
    FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_activity (activity_id),
    INDEX idx_student (student_id),
    INDEX idx_status (status)
);
```

**用途:**
- 学生提交作品
- 教师查看学生提交
- 作业跟踪

---

#### **12. Assessments 表 - 评估**
```sql
CREATE TABLE assessments (
    assessment_id INT PRIMARY KEY AUTO_INCREMENT,
    submission_id INT NOT NULL,
    teacher_id INT NOT NULL,
    grade VARCHAR(10),
    feedback TEXT,
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_submission (submission_id),
    INDEX idx_teacher (teacher_id)
);
```

**用途:**
- 教师评估学生
- 生成学生进度报告
- 反馈管理

---

#### **13. Messages 表 - 消息**
```sql
CREATE TABLE messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    message_text TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP NULL,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_sender (sender_id),
    INDEX idx_recipient (recipient_id),
    INDEX idx_read (read_at)
);
```

**用途:**
- 教师和学生之间的直接消息
- 内部沟通（学校管理、教师、学生）
- 不包括外部利益相关者（已有其他平台）

---

#### **14. Notes 表 - 笔记**
```sql
CREATE TABLE notes (
    note_id INT PRIMARY KEY AUTO_INCREMENT,
    teacher_id INT NOT NULL,
    target_type ENUM('submission', 'content', 'sighting') NOT NULL,
    target_id INT NOT NULL,  -- submission_id, content_id, or sighting_id
    note_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_teacher (teacher_id),
    INDEX idx_target (target_type, target_id)
);
```

**用途:**
- 教师在学生作品上留笔记
- 教师在目击报告上留笔记
- 教师评论和指导

---

#### **15. User_Profiles 表 - 用户资料**
```sql
CREATE TABLE user_profiles (
    profile_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    avatar_path VARCHAR(500),
    color_scheme VARCHAR(50),
    bio TEXT,
    is_public BOOLEAN DEFAULT TRUE,  -- 学生为 FALSE
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user (user_id),
    INDEX idx_public (is_public)
);
```

**用途:**
- 学生个性化（头像、配色）
- 社区成员公开资料
- 隐私保护（学生资料不公开）
- 仅策划的数字库（避免不当内容）

---

#### **16. Creative_Canvas 表 - 创意画布**
```sql
CREATE TABLE creative_canvas (
    canvas_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    program_id INT NOT NULL,
    assets JSON,  -- 编译的材料和资产
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_program (program_id)
);
```

**用途:**
- 学生自我评估贡献
- 作品集创建
- 捕捉独特体验
- 成就展示

---

#### **17. Access_Logs 表 - 访问日志**
```sql
CREATE TABLE access_logs (
    log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(200) NOT NULL,
    target_type VARCHAR(50),
    target_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_action (action)
);
```

**用途:**
- 安全审计
- 监控学生数据访问
- 合规性检查
- 数据保护（仅分配的教师可访问）

---

#### **18. Business_Analytics 表 - 业务分析**
```sql
CREATE TABLE business_analytics (
    analytics_id INT PRIMARY KEY AUTO_INCREMENT,
    metric_type VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2),
    metric_data JSON,  -- 额外的详细数据
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_metric_type (metric_type),
    INDEX idx_recorded_at (recorded_at)
);
```

**用途:**
- 管理层仪表板
- 订阅数据
- 用户行为分析
- 服务可用性跟踪
- 流行服务识别
- 战略决策支持

---

## 功能与数据库映射关系图

### **教师功能映射**
```
管理班级 → classes, organization_members
创建活动 → activities
接纳学生 → class_enrollments
评估学生 → assessments, submissions
发送消息 → messages
留下笔记 → notes
访问材料 → content_library
生成报告 → assessments + class_enrollments (聚合查询)
```

### **学生功能映射**
```
个性化账户 → user_profiles
查看项目 → program_enrollments
提交作业 → submissions
报告目击 → species_sightings
上传作品 → content_library
创建画布 → creative_canvas
消息教师 → messages
回复笔记 → messages (回复笔记的消息)
```

### **校长功能映射**
```
订阅 → organizations (subscription_status)
生成访问码 → organization_members (access_code)
隐私控制 → organizations (is_public), user_profiles (is_public)
高级数据访问 → 通过 organization_members + 角色权限
```

### **系统管理员功能映射**
```
注册组织 → organizations
管理账户 → users, organization_members
业务仪表板 → business_analytics
监控活动 → access_logs
```

### **社区功能映射**
```
注册成员 → organization_members
贡献内容 → content_library (is_public = true)
成员资料 → user_profiles (is_public = true)
社区图书馆 → content_library (org_id = community_id)
```

---

## 关键数据库关系

### **多对多关系**
1. **用户 ↔ 组织** (通过 `organization_members`)
2. **学生 ↔ 班级** (通过 `class_enrollments`)
3. **用户/组织 ↔ 项目** (通过 `program_enrollments`)

### **一对多关系**
1. **教师 → 班级** (`classes.teacher_id`)
2. **班级 → 活动** (`activities.class_id`)
3. **活动 → 提交** (`submissions.activity_id`)
4. **用户 → 内容** (`content_library.created_by`)
5. **用户 → 目击** (`species_sightings.reported_by`)

### **一对一关系**
1. **提交 → 评估** (`assessments.submission_id` UNIQUE)
2. **用户 → 资料** (`user_profiles.user_id` UNIQUE)

---

## 关键安全考虑

### **1. 行级安全**
```sql
-- 学生资料必须对公众隐藏
-- 在 user_profiles 表中：
-- WHERE user_type = 'student' THEN is_public = FALSE

-- 实现示例（应用层逻辑）：
SELECT * FROM user_profiles 
WHERE is_public = TRUE OR user_id = [current_user_id];
```

### **2. 访问控制**
```sql
-- 仅分配的教师可查看其班级学生数据
-- 查询示例：
SELECT s.* FROM submissions s
JOIN class_enrollments ce ON s.student_id = ce.student_id
JOIN classes c ON ce.class_id = c.class_id
WHERE c.teacher_id = [current_teacher_id];
```

### **3. 组织隐私**
```sql
-- 学校：公众只能看到图书馆，不能看到学生资料
-- 社区：公众可以看到图书馆和成员资料

-- 学校图书馆查询（公开）：
SELECT * FROM content_library 
WHERE org_id = [school_id] AND is_public = TRUE;

-- 社区成员查询（公开）：
SELECT u.*, up.* FROM users u
JOIN user_profiles up ON u.user_id = up.user_id
JOIN organization_members om ON u.user_id = om.user_id
WHERE om.org_id = [community_id] AND up.is_public = TRUE;
```

### **4. 数据加密**
- 敏感字段加密：`password_hash`, 儿童个人信息
- 传输加密：HTTPS/TLS
- 静态加密：数据库级别加密

### **5. 审计追踪**
```sql
-- 所有对学生数据的访问必须记录
-- 触发器示例：
CREATE TRIGGER log_student_access
AFTER SELECT ON submissions
FOR EACH ROW
BEGIN
    INSERT INTO access_logs (user_id, action, target_type, target_id, timestamp)
    VALUES (CURRENT_USER(), 'view_submission', 'submission', NEW.submission_id, NOW());
END;
```

### **6. 认证方法**
- 学生：唯一访问码 (`organization_members.access_code`)
- 其他用户：用户名/密码 + 多因素认证（推荐）
- 会话管理：`users.last_login`

---

## 系统可扩展性考虑

### **云平台架构建议**
根据 Tegar Prayudi 的可持续性要求：
```
推荐平台：AWS, Azure, Google Cloud Platform
服务模式：PaaS (Platform as a Service)

关键服务：
- 计算：Auto-scaling 容器（ECS, AKS, GKE）
- 数据库：托管关系数据库（RDS, Azure SQL, Cloud SQL）
- 存储：对象存储（S3, Blob Storage, Cloud Storage）
- CDN：内容分发网络（CloudFront, Azure CDN, Cloud CDN）
- 负载均衡：自动负载均衡器
```

### **数据库扩展策略**
```
1. 读写分离：主从复制
2. 分片策略：按 org_id 分片（学校/社区）
3. 缓存层：Redis/Memcached 用于频繁查询
4. 归档策略：旧数据归档到冷存储
```

---

## ISO 9241-210:2019 合规性映射

### **可用性原则**
| 原则 | 数据库实现 |
|------|-----------|
| 易于学习 | 清晰的表结构、一致的命名约定 |
| 高效 | 优化的索引、减少连接查询 |
| 容错 | 约束、触发器防止无效数据 |

### **交互性原则**
| 原则 | 数据库实现 |
|------|-----------|
| 视觉呈现 | `user_profiles` 支持主题和配色 |
| 个性化 | `creative_canvas` 捕捉独特体验 |
| 灵活活动 | `activities` 表支持多种活动类型 |

---

## 示例查询

### **1. 教师查看其班级学生进度**
```sql
SELECT 
    u.username AS student_name,
    c.class_name,
    a.activity_name,
    s.submission_date,
    ass.grade,
    ass.feedback
FROM users u
JOIN class_enrollments ce ON u.user_id = ce.student_id
JOIN classes c ON ce.class_id = c.class_id
JOIN activities a ON c.class_id = a.class_id
LEFT JOIN submissions s ON a.activity_id = s.activity_id AND s.student_id = u.user_id
LEFT JOIN assessments ass ON s.submission_id = ass.submission_id
WHERE c.teacher_id = [current_teacher_id]
ORDER BY c.class_name, u.username, a.activity_name;
```

### **2. 公众浏览社区图书馆和成员**
```sql
-- 社区图书馆
SELECT 
    cl.*,
    u.username AS author
FROM content_library cl
JOIN users u ON cl.created_by = u.user_id
WHERE cl.org_id = [community_id] AND cl.is_public = TRUE
ORDER BY cl.created_at DESC;

-- 社区成员资料
SELECT 
    u.username,
    up.bio,
    up.avatar_path
FROM users u
JOIN user_profiles up ON u.user_id = up.user_id
JOIN organization_members om ON u.user_id = om.user_id
WHERE om.org_id = [community_id] AND up.is_public = TRUE;
```

### **3. 公众浏览学校图书馆（不包括学生资料）**
```sql
-- 仅学校图书馆，无学生个人信息
SELECT 
    cl.title,
    cl.content_type,
    cl.content_data,
    cl.created_at
FROM content_library cl
WHERE cl.org_id = [school_id] AND cl.is_public = TRUE
ORDER BY cl.created_at DESC;

-- 注意：不包括创建者信息以保护学生隐私
```

### **4. 学生查看个人创意画布**
```sql
SELECT 
    cc.*,
    p.program_name
FROM creative_canvas cc
JOIN programs p ON cc.program_id = p.program_id
WHERE cc.user_id = [current_student_id]
ORDER BY cc.updated_at DESC;
```

### **5. 管理层业务仪表板数据**
```sql
-- 订阅统计
SELECT 
    org_type,
    subscription_status,
    COUNT(*) AS count
FROM organizations
GROUP BY org_type, subscription_status;

-- 用户人口统计
SELECT 
    user_type,
    COUNT(*) AS total_users
FROM users
GROUP BY user_type;

-- 热门项目
SELECT 
    p.program_name,
    COUNT(pe.enrollment_id) AS enrollment_count
FROM programs p
LEFT JOIN program_enrollments pe ON p.program_id = pe.program_id
WHERE pe.status = 'active'
GROUP BY p.program_id
ORDER BY enrollment_count DESC
LIMIT 10;
```

---

## 总结

该数据库设计支持 Komodo Hub 的所有关键功能：

✅ **用户管理**: 10 种用户类型，明确的角色和权限  
✅ **隐私保护**: 学生数据保护，公开/私有控制  
✅ **教育功能**: 班级、活动、提交、评估  
✅ **社区参与**: 社区图书馆、成员贡献  
✅ **保护工作**: 物种目击报告、保护项目  
✅ **安全合规**: 访问日志、审计追踪、加密  
✅ **可扩展性**: 支持云平台部署、自动扩展  
✅ **业务智能**: 分析仪表板、战略决策支持  

该设计遵循 ISO 9241-210:2019 原则，专注于可用性、交互性、可持续性和系统安全。
