<template>
  <div class="home-container">
    <el-container class="main-container">
      <!-- 侧边栏 -->
      <el-aside width="200px">
        <div class="logo">
          <h2>TronSync</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="side-menu"
          @select="handleMenuSelect"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="dashboard">
            <el-icon><component :is="User" /></el-icon>
            <span>个人信息</span>
          </el-menu-item>
          <el-menu-item index="courses">
            <el-icon><component :is="Reading" /></el-icon>
            <span>我的课程</span>
          </el-menu-item>
          <el-menu-item index="schedule">
            <el-icon><component :is="Calendar" /></el-icon>
            <span>课程表</span>
          </el-menu-item>
          <el-menu-item index="announcements">
            <el-icon><component :is="Bell" /></el-icon>
            <span>公告</span>
            <el-badge v-if="unreadCount > 0" :value="unreadCount" class="badge-item" />
          </el-menu-item>
          <el-menu-item index="files">
            <el-icon><component :is="FolderOpened" /></el-icon>
            <span>文件库</span>
          </el-menu-item>
          <el-menu-item index="contacts">
            <el-icon><component :is="Message" /></el-icon>
            <span>联系</span>
          </el-menu-item>
        </el-menu>
        
        <div class="logout-section">
          <el-button type="info" text @click="openAbout">
            <el-icon><InfoFilled /></el-icon>
            关于
          </el-button>
          <el-button type="info" text @click="openSettings">
            <el-icon><Setting /></el-icon>
            设置
          </el-button>
          <el-button type="danger" text @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            退出登录
          </el-button>
        </div>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-main>
        <div class="content-header">
          <h2>{{ currentTitle }}</h2>
          <div class="header-actions" style="display: flex; align-items: center; gap: 12px;">
            <el-button 
              @click="toggleTheme" 
              circle 
              :title="themeStore.themeMode === 'dark' ? '切换浅色模式' : '切换深色模式'"
            >
              <el-icon>
                <component :is="themeStore.themeMode === 'dark' ? Moon : Sunny" />
              </el-icon>
            </el-button>
            <el-button @click="loadData(true)" :loading="loading" circle title="强制刷新">
              <el-icon><component :is="Refresh" /></el-icon>
            </el-button>
          </div>
        </div>
        
        <el-scrollbar class="content-body">
          <Transition name="fade-slide" mode="out-in">
            <!-- 个人信息 Dashboard -->
            <div v-if="activeMenu === 'dashboard'" key="dashboard" class="dashboard-view">
              <!-- 个人信息卡片 -->
              <el-card class="profile-card" shadow="hover">
              <div class="profile-header">
                <el-avatar :size="80" :src="userProfile.avatar_url || '/default-avatar.png'" />
                <div class="profile-info">
                  <h2>{{ userProfile.name || '未知' }}</h2>
                  <p class="student-id">学号：{{ userProfile.student_id || '未知' }}</p>
                  <p class="email">{{ userProfile.email || '未知' }}</p>
                </div>
              </div>
              <el-divider />
              <el-descriptions :column="2" border>
                <el-descriptions-item label="专业">{{ userProfile.major || '未知' }}</el-descriptions-item>
                <el-descriptions-item label="平台角色">{{ userProfile.platform_role || '未知' }}</el-descriptions-item>
              </el-descriptions>
            </el-card>

            <!-- 快捷入口卡片 -->
            <div class="quick-access-grid">
              <!-- 课程表卡片 -->
              <el-card class="quick-card schedule-card" shadow="hover" @click="navigateTo('schedule')">
                <div class="card-icon">
                  <el-icon :size="40"><Calendar /></el-icon>
                </div>
                <div class="card-content">
                  <h3>查看课程表</h3>
                  <p>查看本周课程安排</p>
                </div>
                <el-icon class="card-arrow"><ArrowRight /></el-icon>
              </el-card>

              <!-- 公告卡片 -->
              <el-card class="quick-card announcement-card" shadow="hover" @click="navigateTo('announcements')">
                <div class="card-icon">
                  <el-icon :size="40"><Bell /></el-icon>
                  <el-badge v-if="unreadCount > 0" :value="unreadCount" class="card-badge" />
                </div>
                <div class="card-content">
                  <h3>公告通知</h3>
                  <p>共有 {{ announcements.length }} 条公告，{{ unreadCount }} 条未读</p>
                </div>
                <el-icon class="card-arrow"><ArrowRight /></el-icon>
              </el-card>

              <!-- 文件库卡片 -->
              <el-card class="quick-card files-card" shadow="hover" @click="navigateTo('files')">
                <div class="card-icon">
                  <el-icon :size="40"><FolderOpened /></el-icon>
                </div>
                <div class="card-content">
                  <h3>文件库</h3>
                  <p>共有 {{ files.length }} 个文件</p>
                </div>
                <el-icon class="card-arrow"><ArrowRight /></el-icon>
              </el-card>

              <!-- 课程学习卡片 -->
              <el-card class="quick-card courses-card" shadow="hover" @click="navigateTo('courses')">
                <div class="card-icon">
                  <el-icon :size="40"><Reading /></el-icon>
                </div>
                <div class="card-content">
                  <h3>我的课程</h3>
                  <p v-if="courses.length > 0">
                    正在学习：{{ courses.slice(0, 3).map(c => c.name).join('、') }}
                    {{ courses.length > 3 ? '等' : '' }}，加油！！
                  </p>
                  <p v-else>暂无课程</p>
                </div>
                <el-icon class="card-arrow"><ArrowRight /></el-icon>
              </el-card>
              
              <!-- 关于卡片 -->
              <el-card class="quick-card about-card" shadow="hover" @click="openAbout">
                <div class="card-icon">
                  <el-icon :size="40"><InfoFilled /></el-icon>
                </div>
                <div class="card-content">
                  <h3>关于 TronSync</h3>
                  <p>查看应用版本和使用说明</p>
                </div>
                <el-icon class="card-arrow"><ArrowRight /></el-icon>
              </el-card>
            </div>
          </div>
          
          <!-- 课程列表 -->
          <div v-else-if="activeMenu === 'courses'" key="courses" class="courses-view">
            <el-row :gutter="20">
              <el-col :span="8" v-for="course in courses" :key="course.id">
                <el-card class="course-card" shadow="hover">
                  <h3>{{ course.name }}</h3>
                  <p class="course-code">课程代码：{{ course.code }}</p>
                  <el-divider />
                  <p><el-icon><component :is="User" /></el-icon> 教师：{{ course.teacher }}</p>
                  <p><el-icon><component :is="CreditCard" /></el-icon> 学分：{{ course.credits }}</p>
                </el-card>
              </el-col>
            </el-row>
            <el-empty v-if="courses.length === 0 && !loading" description="暂无课程数据" />
          </div>
          
          <!-- 课程表 -->
          <div v-else-if="activeMenu === 'schedule'" key="schedule" class="schedule-view">
            <!-- 学年/学期/周数控制栏 -->
            <div class="semester-control">
              <!-- 学年切换 -->
              <div class="control-group">
                <label>学年：</label>
                <el-button-group size="small">
                  <el-button @click="changeAcademicYear(-1)">
                    <el-icon><ArrowLeft /></el-icon>
                  </el-button>
                  <el-button disabled>{{ currentAcademicYear }}学年</el-button>
                  <el-button @click="changeAcademicYear(1)">
                    <el-icon><ArrowRight /></el-icon>
                  </el-button>
                </el-button-group>
              </div>
              
              <!-- 学期切换 -->
              <div class="control-group">
                <label>学期：</label>
                <el-radio-group v-model="currentSemester" size="small" @change="changeSemester">
                  <el-radio-button :label="1">第一学期</el-radio-button>
                  <el-radio-button :label="2">第二学期</el-radio-button>
                </el-radio-group>
              </div>
              
              <!-- 周数切换 -->
              <div class="control-group">
                <el-button-group size="small">
                  <el-button @click="changeWeek(-1)" :disabled="currentWeek <= 1">
                    <el-icon><ArrowLeft /></el-icon>
                    上一周
                  </el-button>
                  <el-button @click="changeWeek(1)" :disabled="currentWeek >= SemesterManager.getSemesterWeeks(currentSemester)">
                    下一周
                    <el-icon><ArrowRight /></el-icon>
                  </el-button>
                </el-button-group>
                
                <div class="week-input">
                  <span>第</span>
                  <el-input-number 
                    v-model="currentWeek" 
                    :min="1" 
                    :max="SemesterManager.getSemesterWeeks(currentSemester)" 
                    size="small"
                    style="width: 70px; margin: 0 4px;"
                    @change="onWeekChange"
                  />
                  <span>周</span>
                </div>
                
                <el-button size="small" type="primary" @click="goToCurrentWeek">
                  <el-icon><Calendar /></el-icon>
                  本周
                </el-button>
              </div>
            </div>
            
            <!-- 课程表格 -->
            <div v-if="schedules.length > 0" class="schedule-table-wrapper">
              <table class="schedule-grid">
                <thead>
                  <tr>
                    <th class="time-header">时间</th>
                    <th v-for="(day, index) in weekDays" :key="day.value" class="day-header">
                      <div class="day-info">
                        <div class="day-name">{{ day.label }}</div>
                        <div class="day-date">{{ formatDateDisplay(weekDates[index]) }}</div>
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="slot in timeSlots" :key="slot.id">
                    <td class="time-cell">
                      <div class="time-label">{{ slot.label }}</div>
                      <div class="time-range">{{ slot.time }}</div>
                    </td>
                    <td v-for="day in weekDays" :key="day.value" class="course-cell">
                      <div 
                        v-for="course in getCourseForSlot(day.value, slot.id)" 
                        :key="`${course.course_name}-${course.start_time}`"
                        class="course-block"
                        :class="getCourseColorClass(course.course_name)"
                        @click="showCourseDetail(course)"
                      >
                        <div class="course-name">{{ course.course_name }}</div>
                        <div class="course-location">{{ course.classroom }}</div>
                        <div class="course-teacher">{{ course.teacher }}</div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <el-empty v-else-if="!loading" description="暂无课程表数据" />
          </div>
          
          <!-- 公告列表 -->
          <div v-else-if="activeMenu === 'announcements'" key="announcements" class="announcements-view">
            <div v-if="announcements.length > 0" class="announcements-list">
              <el-card 
                v-for="(announcement, index) in announcements" 
                :key="announcement.id || `announcement-${index}`"
                class="announcement-card"
                shadow="hover"
              >
                <div class="announcement-header" @click.stop="toggleAnnouncement(announcement.id || `announcement-${index}`)">
                  <div class="announcement-title-row">
                    <h4>{{ announcement.title }}</h4>
                    <el-icon class="expand-icon" :class="{ 'expanded': expandedAnnouncements.includes(announcement.id || `announcement-${index}`) }">
                      <component :is="ArrowDown" />
                    </el-icon>
                  </div>
                  <div class="announcement-meta">
                    <el-tag size="small" type="primary">{{ announcement.course_name }}</el-tag>
                    <span class="announcement-time">{{ announcement.publish_time }}</span>
                  </div>
                </div>
                
                <el-collapse-transition>
                  <div v-show="expandedAnnouncements.includes(announcement.id || `announcement-${index}`)" class="announcement-content" @click.stop="handleContentClick">
                    <el-divider />
                    <div v-html="formatAnnouncementContent(announcement.content)" class="content-html"></div>
                  </div>
                </el-collapse-transition>
              </el-card>
            </div>
            <el-empty v-else-if="!loading" description="暂无公告" />
          </div>
          
          <!-- 文件库 -->
          <div v-else-if="activeMenu === 'files'" key="files" class="files-view">
            <!-- 面包屑导航 -->
            <div class="breadcrumb-nav">
              <el-breadcrumb separator="/">
                <el-breadcrumb-item 
                  v-for="(item, index) in breadcrumb" 
                  :key="item.id"
                  :class="{ 'is-active': index === breadcrumb.length - 1 }"
                >
                  <a 
                    v-if="index < breadcrumb.length - 1" 
                    @click.prevent="navigateToBreadcrumb(item)"
                    href="javascript:void(0)"
                  >
                    {{ item.name }}
                  </a>
                  <span v-else>{{ item.name }}</span>
                </el-breadcrumb-item>
              </el-breadcrumb>
            </div>
            
            <div v-if="files.length > 0" class="files-list">
              <el-table :data="files" stripe style="width: 100%">
                <el-table-column prop="name" label="文件名" width="300">
                  <template #default="{ row }">
                    <div class="file-item">
                      <el-icon :size="20" style="margin-right: 8px;">
                        <component :is="Folder" v-if="row.type === 'folder'" />
                        <component :is="Document" v-else-if="row.type === 'pdf'" />
                        <component :is="Document" v-else-if="row.type === 'docx'" />
                        <component :is="Document" v-else-if="row.type === 'xlsx'" />
                        <component :is="Document" v-else-if="row.type === 'pptx'" />
                        <component :is="Document" v-else />
                      </el-icon>
                      <span>{{ row.name }}</span>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="type" label="类型" width="100" />
                <el-table-column label="大小" width="120">
                  <template #default="{ row }">
                    {{ formatFileSize(row.size) }}
                  </template>
                </el-table-column>
                <el-table-column prop="created_at" label="上传时间" width="150" />
                <el-table-column prop="reference_count" label="引用数" width="100" />
                <el-table-column label="操作" width="150">
                  <template #default="{ row }">
                    <el-button 
                      v-if="row.type !== 'folder' && row.allow_download" 
                      size="small" 
                      type="primary" 
                      @click="downloadFile(row)"
                    >
                      下载
                    </el-button>
                    <el-button 
                      v-else-if="row.type === 'folder'" 
                      size="small" 
                      @click="openFolder(row)"
                    >
                      打开
                    </el-button>
                    <el-button 
                      size="small" 
                      @click="renameFile(row)"
                    >
                      重命名
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <el-empty v-else-if="!loading" description="暂无文件" />
          </div>
          
          <!-- 联系页面 -->
          <div v-else-if="activeMenu === 'contacts'" key="contacts" class="contacts-view">
            <Contacts />
          </div>
          </Transition>
        </el-scrollbar>
      </el-main>
    </el-container>
    
    <!-- 设置对话框 -->
    <el-dialog
      v-model="settingsVisible"
      title="设置"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="settings" label-width="120px">
        <!-- 外观设置 -->
        <el-divider content-position="left">
          <el-icon><component :is="Setting" /></el-icon>
          外观设置
        </el-divider>
        
        <el-form-item label="主题模式">
          <el-radio-group v-model="themeStore.themeMode" @change="themeStore.applyTheme">
            <el-radio label="light">浅色</el-radio>
            <el-radio label="dark">深色</el-radio>
            <el-radio label="auto">跟随系统</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="主题颜色">
          <div class="theme-colors">
            <div 
              v-for="theme in themeStore.presetThemes" 
              :key="theme.color"
              class="color-block"
              :style="{ backgroundColor: theme.color }"
              :class="{ active: themeStore.themeColor === theme.color }"
              @click="themeStore.setColor(theme.color)"
              :title="theme.name"
            >
              <el-icon v-if="themeStore.themeColor === theme.color" color="#fff"><component :is="Check" /></el-icon>
            </div>
            <el-color-picker v-model="themeStore.themeColor" @change="themeStore.setColor" />
          </div>
        </el-form-item>
        
        <el-form-item label="紧凑模式">
          <el-switch v-model="settings.compactMode" @change="applyCompactMode" />
          <span style="margin-left: 12px; color: #909399; font-size: 12px;">
            减少间距，显示更多内容
          </span>
        </el-form-item>
        
        <!-- 功能设置 -->
        <el-divider content-position="left">
          <el-icon><component :is="FolderOpened" /></el-icon>
          功能设置
        </el-divider>
        
        <el-form-item label="下载路径">
          <el-input 
            v-model="settings.downloadPath" 
            placeholder="留空使用默认下载路径"
            style="width: 100%;"
          >
            <template #append>
              <el-button @click="selectDownloadPath">选择</el-button>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="自动刷新">
          <el-input-number 
            v-model="settings.autoRefreshInterval" 
            :min="0" 
            :max="60"
            style="width: 120px;"
          />
          <span style="margin-left: 8px;">分钟（0表示关闭）</span>
        </el-form-item>
        
        <el-form-item label="启动自动登录">
          <el-switch v-model="settings.autoLogin" />
        </el-form-item>
        
        <!-- 通知设置 -->
        <el-divider content-position="left">
          <el-icon><component :is="Bell" /></el-icon>
          通知设置
        </el-divider>
        
        <el-form-item label="新公告提醒">
          <el-switch v-model="settings.notifyNewAnnouncement" />
        </el-form-item>
        
        <el-form-item label="课程提醒">
          <el-switch v-model="settings.notifyCourse" />
          <span style="margin-left: 12px; color: #909399; font-size: 12px;">
            上课前15分钟提醒
          </span>
        </el-form-item>
        
        <!-- 缓存管理 -->
        <el-divider content-position="left">
          <el-icon><component :is="Refresh" /></el-icon>
          缓存管理
        </el-divider>
        
        <el-form-item label="清除缓存">
          <el-button type="warning" @click="clearCache">清除所有缓存数据</el-button>
          <div style="margin-top: 8px; color: #909399; font-size: 12px;">
            清除后需要重新加载数据
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="settingsVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
      </template>
    </el-dialog>
    
    <!-- 关于对话框 -->
    <el-dialog
      v-model="aboutVisible"
      title="关于 TronSync"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="about-content">
        <!-- 应用信息 -->
        <div class="about-section">
          <div class="app-logo">
            <el-icon :size="60" color="#409eff"><Reading /></el-icon>
          </div>
          <h2 class="app-name">TronSync</h2>
          <p class="app-version">版本 1.1.0</p>
          <p class="app-description">澳门城市大学校园助手</p>
        </div>
        
        <el-divider />
        
        <!-- 爬虫声明 -->
        <div class="about-section">
          <h3><el-icon><WarningFilled /></el-icon> 爬虫声明</h3>
          <div class="declaration-box">
            <p><strong>TronSync 已实现良好的请求限制和浏览器伪装：</strong></p>
            <ul>
              <li>✅ 合理的请求频率控制，不会对服务器造成压力</li>
              <li>✅ 完整的浏览器 User-Agent 伪装</li>
              <li>✅ 遵循网站的访问规则</li>
              <li>✅ 仅用于个人学习和数据查看</li>
            </ul>
            
            <p class="warning-text">
              <el-icon><WarningFilled /></el-icon>
              <strong>使用提醒：</strong>
            </p>
            <ul>
              <li>⚠️ 请勿频繁刷新数据（建议间隔 5 分钟以上）</li>
              <li>⚠️ 请勿在短时间内重复登录</li>
              <li>⚠️ 请勿将本应用用于商业用途</li>
              <li>⚠️ 请妥善保管您的账号密码</li>
            </ul>
            
            <p class="note-text">
              本应用仅供学习交流使用，请合理使用，尊重学校网站资源。
            </p>
          </div>
        </div>
        
        <el-divider />
        
        <!-- 链接 -->
        <div class="about-section">
          <h3><el-icon><Link /></el-icon> 相关链接</h3>
          <div class="links-box">
            <el-button type="primary" @click="openGitHub" style="width: 100%;">
              <el-icon><component :is="'svg'" viewBox="0 0 1024 1024">
                <path d="M512 42.666667A464.64 464.64 0 0 0 42.666667 502.186667 460.373333 460.373333 0 0 0 363.52 938.666667c23.466667 4.266667 32-9.813333 32-22.186667v-78.08c-130.56 27.733333-158.293333-61.44-158.293333-61.44a122.026667 122.026667 0 0 0-52.053334-67.413333c-42.666667-28.16 3.413333-27.733333 3.413334-27.733334a98.56 98.56 0 0 1 71.68 47.36 101.12 101.12 0 0 0 136.533333 37.973334 99.413333 99.413333 0 0 1 29.866667-61.44c-104.106667-11.52-213.333333-50.773333-213.333334-226.986667a177.066667 177.066667 0 0 1 47.36-124.16 161.28 161.28 0 0 1 4.693334-121.173333s39.68-12.373333 128 46.933333a455.68 455.68 0 0 1 234.666666 0c89.6-59.306667 128-46.933333 128-46.933333a161.28 161.28 0 0 1 4.693334 121.173333A177.066667 177.066667 0 0 1 810.666667 477.866667c0 176.64-110.08 215.466667-213.333334 226.986666a106.666667 106.666667 0 0 1 32 85.333334v126.293333c0 14.933333 8.533333 26.88 32 22.186667A460.8 460.8 0 0 0 981.333333 502.186667 464.64 464.64 0 0 0 512 42.666667" fill="currentColor"/>
              </component></el-icon>
              GitHub 仓库
            </el-button>
            
            <p class="github-note">
              欢迎 Star ⭐ 和提交 Issue
            </p>
          </div>
        </div>
        
        <el-divider />
        
        <!-- 版本更新 -->
        <div class="about-section">
          <h3><el-icon><Refresh /></el-icon> 检查更新</h3>
          <div class="update-box">
            <div v-if="updateStatus === 'checking'" class="update-status">
              <el-icon class="is-loading"><Loading /></el-icon> 正在检查更新...
            </div>
            <div v-else-if="updateStatus === 'has-update'" class="update-info">
              <el-tag type="success" effect="dark">发现新版本 {{ newVersion }}</el-tag>
              <p class="release-date">发布时间: {{ releaseDate }}</p>
              <div class="release-notes" v-html="releaseNotes"></div>
              <el-button type="primary" :loading="updating" @click="doUpdate">
                {{ updating ? '正在下载更新...' : '立即更新并重启' }}
              </el-button>
            </div>
            <div v-else-if="updateStatus === 'no-update'" class="update-status">
              <el-icon color="#67C23A"><CircleCheckFilled /></el-icon> 当前已是最新版本
            </div>
            <div v-else class="update-action">
              <p>当前版本: v1.0.0</p>
              <el-button @click="checkUpdate">检查更新</el-button>
            </div>
          </div>
        </div>

        <el-divider />
        
        <!-- 技术栈 -->
        <div class="about-section">
          <h3><el-icon><Tools /></el-icon> 技术栈</h3>
          <div class="tech-stack">
            <el-tag>Vue 3</el-tag>
            <el-tag type="success">Element Plus</el-tag>
            <el-tag type="warning">Flask</el-tag>
            <el-tag type="danger">PyWebView</el-tag>
            <el-tag type="info">BeautifulSoup</el-tag>
          </div>
        </div>
        
        <el-divider />
        
        <!-- 版权信息 -->
        <div class="about-section copyright">
          <p>© 2025 TronSync. All rights reserved.</p>
          <p>Made with ❤️ for CityU Students</p>
        </div>
      </div>
      
      <template #footer>
        <el-button type="primary" @click="aboutVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Contacts from './Contacts.vue'
import { 
  Reading, 
  Calendar, 
  Bell, 
  User, 
  SwitchButton, 
  Refresh, 
  FolderOpened, 
  Folder, 
  Document, 
  ArrowDown, 
  CreditCard,
  ArrowLeft,
  ArrowRight,
  Setting,
  InfoFilled,
  WarningFilled,
  Link,
  Tools,
  Message,
  Check,
  Sunny,
  Moon,
  Loading,
  CircleCheckFilled
} from '@element-plus/icons-vue'
import api from '../api'
import CacheManager from '../utils/cacheManager'
import SemesterManager from '../utils/semesterManager'
import TIME_SLOTS, { isTimeInSlot, calculateSpanSlots } from '../utils/timeSlots'
import { useThemeStore } from '../store/theme'

const router = useRouter()
const themeStore = useThemeStore()
const loading = ref(false)
const activeMenu = ref('dashboard')  // 默认显示个人信息
const expandedAnnouncements = ref([])  // 记录展开的公告
const unreadCount = ref(0)  // 未读公告数量
const settingsVisible = ref(false)  // 设置对话框显示状态
const aboutVisible = ref(false)  // 关于对话框显示状态

// 设置项
const settings = reactive({
  compactMode: false,
  downloadPath: '',
  autoRefreshInterval: 5,  // 分钟
  autoLogin: false,
  notifyNewAnnouncement: true,
  notifyCourse: false
})

const dataLoaded = ref({
  courses: false,
  schedule: false,
  announcements: false,
  profile: false,
  files: false
})

const courses = ref([])
const schedules = ref([])
const announcements = ref([])
const files = ref([])  // 确保初始化为空数组
const breadcrumb = ref([{ id: 0, name: '根目录' }])
const currentFolderId = ref(0)

// 学年/学期/周数管理
const currentAcademicYear = ref(2025)
const currentSemester = ref(1)
const currentWeek = ref(1)
const weekDates = ref([])  // 当前周的日期数组

const userProfile = reactive({
  name: '',
  student_id: '',
  email: '',
  major: ''
})

// 星期数据（周日到周六）
const weekDays = [
  { value: 7, label: '周日', shortLabel: '日' },
  { value: 1, label: '周一', shortLabel: '一' },
  { value: 2, label: '周二', shortLabel: '二' },
  { value: 3, label: '周三', shortLabel: '三' },
  { value: 4, label: '周四', shortLabel: '四' },
  { value: 5, label: '周五', shortLabel: '五' },
  { value: 6, label: '周六', shortLabel: '六' }
]

// 简化的时间段（10个大时间段）
const timeSlots = [
  { id: 1, label: '第1节', time: '08:00-09:00' },
  { id: 2, label: '第2节', time: '09:00-10:00' },
  { id: 3, label: '第3节', time: '10:00-11:00' },
  { id: 4, label: '第4节', time: '11:00-12:00' },
  { id: 5, label: '第5节', time: '12:00-13:00' },
  { id: 6, label: '第6节', time: '13:00-14:00' },
  { id: 7, label: '第7节', time: '14:00-15:00' },
  { id: 8, label: '第8节', time: '15:00-16:00' },
  { id: 9, label: '第9节', time: '16:00-17:00' },
  { id: 10, label: '第10节', time: '17:00-18:00' },
  { id: 11, label: '第11节', time: '18:00-19:00' },
  { id: 12, label: '第12节', time: '19:00-20:00' },
  { id: 13, label: '第13节', time: '20:00-21:00' },
  { id: 14, label: '第14节', time: '21:00-22:00' }
]

const currentTitle = computed(() => {
  const titles = {
    dashboard: '个人信息',
    courses: '我的课程',
    schedule: '课程表',
    announcements: '公告',
    files: '文件库',
    contacts: '联系'
  }
  return titles[activeMenu.value] || ''
})

// 初始化学年学期周数
const initializeSemester = () => {
  const current = SemesterManager.getCurrentWeek()
  currentAcademicYear.value = current.academicYear
  currentSemester.value = current.semester
  currentWeek.value = current.week
  updateWeekDates()
}

// 更新当前周的日期
const updateWeekDates = () => {
  const weekInfo = SemesterManager.getWeekDates(
    currentAcademicYear.value,
    currentSemester.value,
    currentWeek.value
  )
  weekDates.value = weekInfo.dates
}

// 切换学年
const changeAcademicYear = (delta) => {
  currentAcademicYear.value += delta
  currentWeek.value = 1
  updateWeekDates()
}

// 切换学期
const changeSemester = (semester) => {
  currentSemester.value = semester
  currentWeek.value = 1
  updateWeekDates()
}

// 切换周数
const changeWeek = (delta) => {
  const maxWeeks = SemesterManager.getSemesterWeeks(currentSemester.value)
  const newWeek = currentWeek.value + delta
  if (newWeek >= 1 && newWeek <= maxWeeks) {
    currentWeek.value = newWeek
    updateWeekDates()
  }
}

// 周数改变时的处理
const onWeekChange = (value) => {
  updateWeekDates()
}

// 跳转到本周
const goToCurrentWeek = () => {
  const current = SemesterManager.getCurrentWeek()
  currentAcademicYear.value = current.academicYear
  currentSemester.value = current.semester
  currentWeek.value = current.week
  updateWeekDates()
}

// 获取指定星期和时间段的课程
const getCourseForSlot = (weekDay, slotId) => {
  return schedules.value.filter(course => {
    if (course.week_day !== weekDay) return false
    
    // 简单匹配：检查课程的开始时间是否在这个时间段内
    const slot = timeSlots.find(s => s.id === slotId)
    if (!slot) return false
    
    const [slotStart] = slot.time.split('-')
    const courseStart = course.start_time
    
    if (!courseStart) return false
    
    // 简单比较时间（HH:MM格式）
    return courseStart.substring(0, 5) >= slotStart && courseStart.substring(0, 5) < getNextSlotTime(slotStart)
  })
}

// 获取下一个时间段的开始时间
const getNextSlotTime = (time) => {
  const [h, m] = time.split(':').map(Number)
  const nextHour = h + 1
  return `${String(nextHour).padStart(2, '0')}:${String(m).padStart(2, '0')}`
}

// 根据课程名称获取颜色类
const getCourseColorClass = (courseName) => {
  const hash = courseName.split('').reduce((acc, char) => {
    return char.charCodeAt(0) + ((acc << 5) - acc)
  }, 0)
  const colorIndex = Math.abs(hash) % 8
  return `course-color-${colorIndex}`
}

// 显示课程详情
const showCourseDetail = (course) => {
  ElMessageBox.alert(
    `<div style="line-height: 1.8;">
      <p><strong>课程名称：</strong>${course.course_name}</p>
      <p><strong>授课教师：</strong>${course.teacher}</p>
      <p><strong>上课地点：</strong>${course.classroom}</p>
      <p><strong>上课时间：</strong>${course.start_time} - ${course.end_time}</p>
      ${course.weeks ? `<p><strong>周次：</strong>${course.weeks}</p>` : ''}
      ${course.course_type ? `<p><strong>课程类型：</strong>${course.course_type}</p>` : ''}
      ${course.credits ? `<p><strong>学分：</strong>${course.credits}</p>` : ''}
    </div>`,
    '课程详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '确定'
    }
  )
}

// 格式化日期显示
const formatDateDisplay = (date) => {
  if (!date) return ''
  return SemesterManager.formatDate(date)
}

const handleMenuSelect = (index) => {
  activeMenu.value = index
  
  // 如果切换到公告页面，标记所有公告为已读
  if (index === 'announcements') {
    markAnnouncementsAsRead()
  }
  
  // 只在数据未加载时才加载，避免频繁请求
  if (!dataLoaded.value[index] && index !== 'contacts') {
    loadData(false)
  } else {
    console.log(`📦 使用已加载的数据: ${index}`)
  }
}

// 导航到指定页面
const navigateTo = (page) => {
  activeMenu.value = page
  handleMenuSelect(page)
}

// 标记公告为已读
const markAnnouncementsAsRead = () => {
  if (announcements.value.length === 0) return
  
  // 获取所有公告ID
  const announcementIds = announcements.value.map(a => a.id || a.title).filter(Boolean)
  
  // 保存到localStorage
  localStorage.setItem('readAnnouncements', JSON.stringify(announcementIds))
  
  // 更新未读数量
  unreadCount.value = 0
  
  console.log('✅ 已标记所有公告为已读')
}

// 计算未读公告数量
const calculateUnreadCount = () => {
  if (announcements.value.length === 0) {
    unreadCount.value = 0
    return
  }
  
  // 从localStorage获取已读公告列表
  const readAnnouncementsStr = localStorage.getItem('readAnnouncements')
  const readAnnouncements = readAnnouncementsStr ? JSON.parse(readAnnouncementsStr) : []
  
  // 计算未读数量
  const unread = announcements.value.filter(a => {
    const id = a.id || a.title
    return id && !readAnnouncements.includes(id)
  })
  
  unreadCount.value = unread.length
  console.log(`📊 未读公告数量: ${unreadCount.value}`)
}

// forceRefresh: 是否强制刷新（点击刷新按钮时）
const toggleTheme = async (event) => {
  const isDark = themeStore.themeMode === 'dark'
  const nextMode = isDark ? 'light' : 'dark'
  
  // 检查浏览器是否支持 View Transitions API
  if (!document.startViewTransition) {
    themeStore.setMode(nextMode)
    return
  }

  // 获取点击位置作为动画圆心
  const x = event.clientX
  const y = event.clientY
  const endRadius = Math.hypot(
    Math.max(x, innerWidth - x),
    Math.max(y, innerHeight - y)
  )

  const transition = document.startViewTransition(async () => {
    themeStore.setMode(nextMode)
    await nextTick()
  })

  transition.ready.then(() => {
    const clipPath = [
      `circle(0px at ${x}px ${y}px)`,
      `circle(${endRadius}px at ${x}px ${y}px)`,
    ]
    
    // 始终在“新”视图上执行扩散动画
    document.documentElement.animate(
      {
        clipPath: clipPath,
      },
      {
        duration: 400,
        easing: 'ease-in',
        pseudoElement: '::view-transition-new(root)',
      }
    )
  })
}

// 监听主题变化，持久化设置
watch(() => themeStore.themeMode, () => {
  saveSettings()
})

const loadData = async (force = false) => {
  loading.value = true
  
  try {
    if (activeMenu.value === 'dashboard') {
      // Dashboard 需要加载所有数据
      await Promise.all([
        loadUserProfile(forceRefresh),
        loadCourses(forceRefresh),
        loadAnnouncements(forceRefresh),
        loadFiles(forceRefresh, 0)
      ])
    } else if (activeMenu.value === 'courses') {
      await loadCourses(forceRefresh)
    } else if (activeMenu.value === 'schedule') {
      await loadSchedule(forceRefresh)
    } else if (activeMenu.value === 'announcements') {
      await loadAnnouncements(forceRefresh)
    } else if (activeMenu.value === 'files') {
      await loadFiles(forceRefresh, 0)
    } else if (activeMenu.value === 'contacts') {
      // 联系页面不需要加载特定数据，因为它使用静态数据
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载课程
const loadCourses = async (forceRefresh = false) => {
  // 先尝试从缓存获取
  const cached = CacheManager.getCache('COURSES', forceRefresh)
  if (cached) {
    courses.value = cached
    dataLoaded.value.courses = true
    return
  }
  
  // 缓存不存在或过期，从服务器获取
  const response = await api.getCourses()
  if (response.success) {
    courses.value = response.data
    CacheManager.setCache('COURSES', response.data)
    dataLoaded.value.courses = true
  }
}

// 加载课程表
const loadSchedule = async (forceRefresh = false) => {
  const cached = CacheManager.getCache('SCHEDULE', forceRefresh)
  if (cached) {
    schedules.value = cached
    dataLoaded.value.schedule = true
    return
  }
  
  const response = await api.getSchedule()
  if (response.success) {
    schedules.value = response.data.schedules
    CacheManager.setCache('SCHEDULE', response.data.schedules)
    dataLoaded.value.schedule = true
  }
}

// 加载公告
const loadAnnouncements = async (forceRefresh = false) => {
  const cached = CacheManager.getCache('ANNOUNCEMENTS', forceRefresh)
  if (cached) {
    announcements.value = cached
    dataLoaded.value.announcements = true
    console.log('📦 使用缓存的公告:', announcements.value.length, '条')
    calculateUnreadCount()
    return
  }
  
  const response = await api.getAnnouncements()
  console.log('📢 公告响应:', response)
  if (response.success) {
    announcements.value = response.data
    console.log('✅ 加载公告成功:', announcements.value.length, '条')
    console.log('📋 第一条公告:', announcements.value[0])
    CacheManager.setCache('ANNOUNCEMENTS', response.data)
    dataLoaded.value.announcements = true
    calculateUnreadCount()
  }
}

// 加载用户信息
const loadUserProfile = async (forceRefresh = false) => {
  const cached = CacheManager.getCache('USER_PROFILE', forceRefresh)
  if (cached) {
    Object.assign(userProfile, cached)
    dataLoaded.value.profile = true
    return
  }
  
  const response = await api.getUserProfile()
  if (response.success) {
    Object.assign(userProfile, response.data)
    CacheManager.setCache('USER_PROFILE', response.data)
    dataLoaded.value.profile = true
  }
}

// 加载文件列表
const loadFiles = async (forceRefresh = false, folderId = null) => {
  try {
    // 如果指定了文件夹ID，使用它；否则使用当前文件夹ID
    const targetFolderId = folderId !== null ? folderId : currentFolderId.value
    
    console.log('📂 加载文件列表, folderId:', targetFolderId)
    
    // 构建缓存键（包含文件夹ID）
    const cacheKey = `FILES_${targetFolderId}`
    
    const cached = CacheManager.getCache(cacheKey, forceRefresh)
    if (cached && cached.files) {
      console.log('📦 使用缓存的文件列表')
      files.value = cached.files || []
      breadcrumb.value = cached.breadcrumb || [{ id: 0, name: '根目录' }]
      currentFolderId.value = targetFolderId
      dataLoaded.value.files = true
      return
    }
    
    console.log('🌐 从服务器获取文件列表')
    const response = await api.getFiles({ parent_id: targetFolderId })
    console.log('📥 服务器响应:', response)
    
    if (response && response.success) {
      files.value = Array.isArray(response.data) ? response.data : []
      breadcrumb.value = Array.isArray(response.breadcrumb) ? response.breadcrumb : [{ id: 0, name: '根目录' }]
      currentFolderId.value = targetFolderId
      
      console.log('✅ 文件列表加载成功:', files.value.length, '个文件')
      console.log('🧭 面包屑:', breadcrumb.value)
      
      // 缓存数据
      CacheManager.setCache(cacheKey, {
        files: files.value,
        breadcrumb: breadcrumb.value
      })
      dataLoaded.value.files = true
    } else {
      console.error('❌ 加载文件列表失败:', response?.message)
      files.value = []
      breadcrumb.value = [{ id: 0, name: '根目录' }]
      ElMessage.error(response?.message || '加载文件列表失败')
    }
  } catch (error) {
    console.error('❌ 加载文件列表异常:', error)
    files.value = []
    breadcrumb.value = [{ id: 0, name: '根目录' }]
    ElMessage.error('加载文件列表失败')
  }
}

// 后台预加载所有数据
const preloadAllData = async () => {
  console.log('🚀 开始后台预加载数据...')
  
  try {
    // 并行加载所有数据（不阻塞界面）
    await Promise.all([
      loadCourses(false),
      loadSchedule(false),
      loadAnnouncements(false),
      loadUserProfile(false),
      loadFiles(false, 0)  // 只预加载根目录
    ])
    
    console.log('✅ 后台预加载完成')
  } catch (error) {
    console.error('❌ 后台预加载失败:', error)
  }
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (!bytes || typeof bytes !== 'number') return '--'
  
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 下载文件
const downloadFile = async (file) => {
  console.log('📥 下载文件:', file.name)
  
  try {
    loading.value = true
    const response = await api.downloadFile(file.id, file.name)
    
    if (response.success) {
      ElMessage.success(`文件已下载到: ${response.path}`)
    } else {
      ElMessage.error('下载失败')
    }
  } catch (error) {
    console.error('下载文件失败:', error)
    ElMessage.error('下载失败')
  } finally {
    loading.value = false
  }
}

// 打开文件夹
const openFolder = async (folder) => {
  console.log('📁 打开文件夹:', folder.name, 'ID:', folder.id)
  
  if (!folder.id) {
    console.error('❌ 文件夹ID无效')
    ElMessage.error('文件夹ID无效')
    return
  }
  
  loading.value = true
  try {
    await loadFiles(false, folder.id)
    console.log('✅ 文件夹打开成功')
  } catch (error) {
    console.error('❌ 打开文件夹失败:', error)
    ElMessage.error('打开文件夹失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 面包屑导航
const navigateToBreadcrumb = async (item) => {
  console.log('🧭 导航到:', item.name, 'ID:', item.id)
  loading.value = true
  try {
    await loadFiles(false, item.id)
    console.log('✅ 导航成功')
  } catch (error) {
    console.error('❌ 导航失败:', error)
    ElMessage.error('导航失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 重命名文件
const renameFile = (file) => {
  console.log('✏️ 重命名文件:', file.name)
  ElMessageBox.prompt('请输入新的文件名:', '重命名', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputValue: file.name
  }).then(({ value }) => {
    console.log('重命名:', file.name, '->', value)
    ElMessage.success('重命名功能开发中...')
  }).catch(() => {
    // 用户取消
  })
}

// 切换公告展开/折叠
const toggleAnnouncement = (id) => {
  console.log('🔄 切换公告:', id)
  const index = expandedAnnouncements.value.indexOf(id)
  if (index > -1) {
    expandedAnnouncements.value.splice(index, 1)
    console.log('➖ 折叠公告:', id, '当前展开:', expandedAnnouncements.value)
  } else {
    expandedAnnouncements.value.push(id)
    console.log('➕ 展开公告:', id, '当前展开:', expandedAnnouncements.value)
  }
}

// 处理内容区域的点击事件
const handleContentClick = (event) => {
  // 检查是否点击的是链接
  const target = event.target
  if (target.tagName === 'A') {
    event.preventDefault()
    const href = target.href || target.getAttribute('href')
    if (href) {
      openExternalLink(href)
    }
  }
}

// 智能打开外部链接
const openExternalLink = (url) => {
  console.log('🔗 打开链接:', url)
  
  // 检查链接类型
  const isTronClass = url.includes('tronclass.cityu.edu.mo')
  const isUrp = url.includes('urp.cityu.edu.mo')
  
  if (isTronClass || isUrp) {
    // 需要认证的链接，提示用户
    ElMessageBox.confirm(
      '该链接需要登录认证，是否在系统浏览器中打开？',
      '打开链接',
      {
        confirmButtonText: '打开',
        cancelButtonText: '取消',
        type: 'info'
      }
    ).then(() => {
      // 在系统浏览器中打开
      window.open(url, '_blank')
      ElMessage.success('已在系统浏览器中打开')
    }).catch(() => {
      // 用户取消
    })
  } else {
    // 普通链接，直接在系统浏览器打开
    window.open(url, '_blank')
  }
}

// 格式化公告内容（处理HTML和链接）
const formatAnnouncementContent = (content) => {
  if (!content) return ''
  
  // 处理换行
  let formatted = content.replace(/\n/g, '<br>')
  
  // 保留链接，但移除target属性（由JS处理点击）
  formatted = formatted.replace(/target="_blank"/g, '')
  formatted = formatted.replace(/target='_blank'/g, '')
  
  return formatted
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await api.logout()
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('username')
    // 清除数据缓存
    CacheManager.clearAllCache()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch (error) {
    // 用户取消
  }
}

// 打开设置对话框
const openSettings = () => {
  loadSettings()
  settingsVisible.value = true
}

// 打开关于对话框
const openAbout = () => {
  aboutVisible.value = true
}

// 更新相关
const updateStatus = ref('initial') // initial, checking, has-update, no-update
const newVersion = ref('')
const releaseNotes = ref('')
const downloadUrl = ref('')
const releaseDate = ref('')
const updating = ref(false)

const checkUpdate = async () => {
  updateStatus.value = 'checking'
  try {
    const res = await api.checkUpdate()
    if (res.has_update) {
      updateStatus.value = 'has-update'
      newVersion.value = res.latest_version
      // 简单处理换行
      releaseNotes.value = res.release_notes ? res.release_notes.replace(/\n/g, '<br>') : '无更新说明'
      downloadUrl.value = res.download_url
      releaseDate.value = new Date(res.release_date).toLocaleString()
    } else {
      updateStatus.value = 'no-update'
    }
  } catch (error) {
    console.error('Check update failed:', error)
    updateStatus.value = 'initial'
    ElMessage.error('检查更新失败: ' + (error.response?.data?.error || error.message))
  }
}

const doUpdate = async () => {
  if (!downloadUrl.value) return
  updating.value = true
  try {
    const res = await api.performUpdate(downloadUrl.value)
    if (res.success) {
      ElMessage.success(res.message)
    } else {
      ElMessage.error('更新失败: ' + res.message)
      updating.value = false
    }
  } catch (error) {
    ElMessage.error('请求更新失败: ' + error.message)
    updating.value = false
  }
}

// 打开 GitHub
const openGitHub = () => {
  window.open('https://github.com', '_blank')
}

// 加载设置
const loadSettings = async () => {
  try {
    const response = await api.getSettings()
    if (response.success && response.data) {
      Object.assign(settings, response.data)
      applyAllSettings()
    }
  } catch (error) {
    console.error('加载设置失败:', error)
  }
}

// 保存设置
const saveSettings = async () => {
  try {
    // 1. 保存到后端 API (Flask)
    const response = await api.saveSettings(settings)
    
    // 2. 保存到本地 Config 文件 (PyWebView)
    if (window.pywebview) {
      try {
        const res = await window.pywebview.api.load_config()
        let config = res.success ? res.data : {}
        if (!config.settings) config.settings = {}
        
        // 合并设置
        Object.assign(config.settings, settings)
        
        // 确保主题设置也同步
        config.settings.themeMode = themeStore.themeMode
        config.settings.themeColor = themeStore.themeColor
        
        await window.pywebview.api.save_config(config)
      } catch (e) {
        console.error('PyWebView 保存配置失败:', e)
      }
    }

    if (response.success || window.pywebview) {
      ElMessage.success('设置已保存')
      settingsVisible.value = false
      applyAllSettings()
    } else {
      ElMessage.error('保存设置失败')
    }
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败')
  }
}



// 应用所有设置
const applyAllSettings = () => {
  themeStore.applyTheme()
  applyCompactMode()
}

// 应用紧凑模式
const applyCompactMode = () => {
  const html = document.documentElement
  if (settings.compactMode) {
    html.classList.add('compact-mode')
  } else {
    html.classList.remove('compact-mode')
  }
}

// 选择下载路径
const selectDownloadPath = async () => {
  try {
    // 使用 pywebview API
    if (window.pywebview) {
      const result = await window.pywebview.api.select_folder()
      if (result.success && result.path) {
        settings.downloadPath = result.path
        ElMessage.success('已选择下载路径')
      } else {
        ElMessage.info('未选择文件夹')
      }
    } else {
      // 如果不在 pywebview 环境中，使用后端 API
      const response = await api.selectFolder()
      if (response.success && response.path) {
        settings.downloadPath = response.path
        ElMessage.success('已选择下载路径')
      } else {
        ElMessage.warning('文件夹选择功能仅在桌面应用中可用')
      }
    }
  } catch (error) {
    console.error('选择文件夹失败:', error)
    ElMessage.error('选择文件夹失败')
  }
}

// 清除缓存
const clearCache = async () => {
  try {
    await ElMessageBox.confirm('确定要清除所有缓存数据吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    CacheManager.clearAllCache()
    localStorage.removeItem('readAnnouncements')
    ElMessage.success('缓存已清除')
    
    // 重新加载数据
    dataLoaded.value = {
      courses: false,
      schedule: false,
      announcements: false,
      profile: false,
      files: false
    }
    loadData(true)
  } catch (error) {
    // 用户取消
  }
}

onMounted(() => {
  // 初始化学年学期周数
  initializeSemester()
  
  // 加载设置
  loadSettings()
  
  // 页面加载时，先加载当前页面
  loadData(false)
  
  // 然后在后台预加载其他数据（不阻塞界面）
  setTimeout(() => {
    preloadAllData()
  }, 1000)
})
</script>

<style>
/* 全局样式 - 深色主题 */
html.dark {
  background: #1a1a1a;
  color: #e0e0e0;
}

html.dark body {
  background: #1a1a1a;
  color: #e0e0e0;
}

html.dark .home-container {
  background: #1a1a1a;
}

html.dark .el-aside {
  background: #2c2c2c !important;
}

html.dark .logo {
  background: #242424 !important;
}

html.dark .el-main {
  background: #1a1a1a !important;
}

html.dark .content-header {
  background: #2c2c2c !important;
  color: #e0e0e0 !important;
}

html.dark .content-header h2 {
  color: #e0e0e0 !important;
}

html.dark .el-card {
  background: #2c2c2c !important;
  border-color: #3a3a3a !important;
  color: #e0e0e0 !important;
}

html.dark .course-card,
html.dark .announcement-card,
html.dark .schedule-view,
html.dark .files-view,
html.dark .dashboard-view {
  background: #2c2c2c !important;
}

html.dark .el-table {
  background: #2c2c2c !important;
  color: #e0e0e0 !important;
}

html.dark .el-table th,
html.dark .el-table td {
  background: #2c2c2c !important;
  color: #e0e0e0 !important;
  border-color: #3a3a3a !important;
}

html.dark .schedule-grid th,
html.dark .schedule-grid td {
  background: #2c2c2c !important;
  color: #e0e0e0 !important;
  border-color: #3a3a3a !important;
}

html.dark .time-cell,
html.dark .time-header {
  background: #242424 !important;
}

html.dark .course-cell {
  background: #1f1f1f !important;
}

html.dark .breadcrumb-nav {
  background: #242424 !important;
}

html.dark .semester-control {
  background: #242424 !important;
}

/* 紧凑模式 */
html.compact-mode .content-body {
  padding: 16px !important;
}

html.compact-mode .el-card {
  margin-bottom: 12px !important;
}

/* 视图切换动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* View Transition API 配置 - 禁用默认动画以启用自定义 clip-path */
::view-transition-old(root),
::view-transition-new(root) {
  animation: none;
  mix-blend-mode: normal;
}

::view-transition-image-pair(root) {
  isolation: isolate;
}
</style>

<style scoped>
.home-container {
  width: 100%;
  height: 100%;
}

.el-container {
  height: 100%;
}

.el-aside {
  background: #545c64;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #434a50;
}

.logo h2 {
  margin: 0;
  font-size: 20px;
  color: #fff;
}

.side-menu {
  flex: 1;
  border: none;
  background: transparent;
}

.logout-section {
  padding: 20px;
  text-align: center;
  border-top: 1px solid #434a50;
}

.main-content {
  background: #f5f5f5;
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-header {
  background: #fff;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 10;
}

.content-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.content-body {
  padding: 30px;
  flex: 1;
  overflow: hidden;
}

.dashboard-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-card {
  max-width: 800px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 16px;
}

.profile-info h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.profile-info .student-id,
.profile-info .email {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
}

.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.quick-card {
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  padding: 24px;
}

.quick-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
}

.quick-card .card-icon {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
  color: #409eff;
}

.quick-card .card-badge {
  position: absolute;
  top: -8px;
  right: -8px;
}

.quick-card .card-content h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #333;
}

.quick-card .card-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

.quick-card .card-arrow {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 20px;
  color: #409eff;
  opacity: 0;
  transition: all 0.3s;
}

.quick-card:hover .card-arrow {
  opacity: 1;
  right: 16px;
}

.schedule-card .card-icon {
  color: #409eff;
}

.announcement-card .card-icon {
  color: #f56c6c;
}

.files-card .card-icon {
  color: #67c23a;
}

.courses-card .card-icon {
  color: #e6a23c;
}

.about-card .card-icon {
  color: #909399;
}

.badge-item {
  margin-left: 8px;
}

/* 关于对话框样式 */
.theme-colors {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}
.color-block {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid transparent;
  transition: all 0.2s;
}
.color-block.active {
  border-color: var(--el-text-color-primary);
  transform: scale(1.1);
  box-shadow: 0 0 4px rgba(0,0,0,0.2);
}

.about-content {
  padding: 20px 0;
}

.about-section {
  margin-bottom: 20px;
  text-align: center;
}

.app-logo {
  margin-bottom: 16px;
}

.app-name {
  font-size: 28px;
  font-weight: bold;
  margin: 8px 0;
  color: #409eff;
}

.app-version {
  font-size: 14px;
  color: #909399;
  margin: 4px 0;
}

.app-description {
  font-size: 16px;
  color: #606266;
  margin: 8px 0;
}

.about-section h3 {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 18px;
  margin-bottom: 16px;
  color: #333;
}

.update-box {
  padding: 10px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  margin-top: 10px;
}

.update-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--el-text-color-regular);
}

.update-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.release-date {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

.release-notes {
  max-height: 150px;
  overflow-y: auto;
  font-size: 13px;
  color: var(--el-text-color-regular);
  background: var(--el-bg-color);
  padding: 8px;
  border-radius: 4px;
  border: 1px solid var(--el-border-color-lighter);
}

.update-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.update-action p {
  margin: 0;
  color: var(--el-text-color-secondary);
}

.declaration-box,
.links-box {
  text-align: left;
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  line-height: 1.8;
}

.declaration-box p {
  margin: 12px 0;
}

.declaration-box ul {
  margin: 8px 0;
  padding-left: 20px;
}

.declaration-box li {
  margin: 6px 0;
}

.warning-text {
  color: #e6a23c;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 16px !important;
}

.note-text {
  color: #909399;
  font-size: 13px;
  margin-top: 16px !important;
  font-style: italic;
}

.github-note {
  text-align: center;
  color: #909399;
  font-size: 13px;
  margin-top: 12px;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.tech-stack .el-tag {
  font-size: 14px;
  padding: 8px 16px;
}

.copyright {
  color: #909399;
  font-size: 13px;
}

.copyright p {
  margin: 4px 0;
}

.course-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-card h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #409eff;
}

.course-code {
  color: #999;
  font-size: 12px;
}

.course-card p {
  margin: 5px 0;
  color: #666;
  display: flex;
  align-items: center;
  gap: 5px;
}

.schedule-view {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.semester-control {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-group label {
  font-weight: 500;
  color: #606266;
  white-space: nowrap;
}

.week-input {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: 12px;
}

.schedule-table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.schedule-grid {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  min-width: 900px;
}

.schedule-grid th,
.schedule-grid td {
  border: 1px solid #e0e0e0;
  padding: 8px;
  text-align: center;
}

.time-header,
.day-header {
  background: #409eff;
  color: #fff;
  font-weight: 600;
  padding: 12px 8px;
}

.time-header {
  width: 100px;
}

.day-header {
  width: calc((100% - 100px) / 7);
}

.day-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.day-name {
  font-size: 14px;
  font-weight: 600;
}

.day-date {
  font-size: 12px;
  opacity: 0.9;
}

.time-cell {
  background: #f5f7fa;
  vertical-align: middle;
}

.time-label {
  font-weight: 600;
  color: #333;
  font-size: 13px;
  margin-bottom: 4px;
}

.time-range {
  color: #666;
  font-size: 11px;
}

.course-cell {
  background: #fafafa;
  vertical-align: top;
  min-height: 60px;
  padding: 4px;
}

.course-block {
  padding: 8px;
  border-radius: 4px;
  margin-bottom: 4px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.course-block:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.course-block:last-child {
  margin-bottom: 0;
}

.course-name {
  font-weight: 600;
  font-size: 12px;
  margin-bottom: 4px;
  color: #fff;
  line-height: 1.3;
}

.course-location,
.course-teacher {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.2;
  margin-top: 2px;
}

/* 课程颜色主题 */
.course-color-0 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.course-color-1 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.course-color-2 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.course-color-3 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.course-color-4 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
.course-color-5 { background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); }
.course-color-6 { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
.course-color-7 { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); }

.announcements-view {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  max-height: calc(100vh - 150px);
  overflow-y: auto;
}

.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.announcement-card {
  transition: all 0.3s;
  border-left: 4px solid #409eff;
}

.announcement-card:hover .announcement-header {
  background-color: #f5f7fa;
}

.announcement-header {
  width: 100%;
  cursor: pointer;
  padding: 4px;
  margin: -4px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.announcement-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.announcement-title-row h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
  flex: 1;
  font-weight: 600;
  word-break: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  line-height: 1.5;
}

.expand-icon {
  transition: transform 0.3s;
  color: #909399;
  font-size: 18px;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

.announcement-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.announcement-time {
  color: #909399;
  font-size: 12px;
}

.announcement-content {
  margin-top: 12px;
}

.content-html {
  color: #666;
  line-height: 1.8;
  font-size: 14px;
  word-break: break-word;
}

.content-html a {
  color: #409eff;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s;
  cursor: pointer;
  pointer-events: auto;
}

.content-html a:hover {
  border-bottom-color: #409eff;
  text-decoration: underline;
}

.content-html p {
  margin: 8px 0;
}

.content-html br {
  margin: 4px 0;
}

.profile-view {
  max-width: 800px;
}

.files-view {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.breadcrumb-nav {
  margin-bottom: 20px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 4px;
}

.breadcrumb-nav .el-breadcrumb {
  font-size: 14px;
}

.breadcrumb-nav a {
  color: #409eff;
  text-decoration: none;
  transition: color 0.3s;
}

.breadcrumb-nav a:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.breadcrumb-nav .is-active span {
  color: #606266;
  font-weight: 500;
}

.files-list {
  min-height: 400px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-item .el-icon {
  vertical-align: middle;
}

.file-item span {
  vertical-align: middle;
  word-break: break-all;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.el-table .el-table__cell {
  padding: 12px 0;
}

.expand-icon {
  transition: transform 0.3s;
  color: #909399;
  font-size: 18px;
  cursor: pointer;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}</style>
