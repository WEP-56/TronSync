<template>
  <div class="contacts-container">
    <h2>联系方式</h2>
    
    <!-- 搜索卡片 -->
    <el-card class="search-card" shadow="hover">
      <div class="search-header" @click="toggleCard('search')">
        <h3>搜索</h3>
        <el-icon class="expand-icon" :class="{ 'expanded': expandedCards.search }">
          <component :is="ArrowDown" />
        </el-icon>
      </div>
      
      <el-collapse-transition>
        <div v-show="expandedCards.search" class="search-content">
          <el-input 
            v-model="searchKeyword" 
            placeholder="输入教师姓名、学院或部门关键字进行搜索..."
            :prefix-icon="Search"
            clearable
          />
          
          <div v-if="searchResults.length > 0" class="search-results">
            <div v-for="result in searchResults" :key="result.id" class="search-result-item">
              <div class="result-type">{{ result.type }}</div>
              <div class="result-name">{{ result.name }}</div>
              <div class="result-contact">{{ result.contact }}</div>
              <div class="result-department">{{ result.department }}</div>
            </div>
          </div>
          <el-empty v-else-if="searchKeyword" description="没有找到相关结果" />
        </div>
      </el-collapse-transition>
    </el-card>
    
    <!-- 教师联系方式卡片 -->
    <el-card class="teachers-card" shadow="hover">
      <div class="card-header" @click="toggleCard('teachers')">
        <h3>教师联系方式</h3>
        <el-icon class="expand-icon" :class="{ 'expanded': expandedCards.teachers }">
          <component :is="ArrowDown" />
        </el-icon>
      </div>
      
      <el-collapse-transition>
        <div v-show="expandedCards.teachers" class="card-content">
          <div v-for="college in colleges" :key="college.name" class="college-section">
            <div class="college-header" @click="toggleCollege(college.name)">
              <h4>{{ college.name }}</h4>
              <el-icon class="expand-icon" :class="{ 'expanded': expandedColleges[college.name] }">
                <component :is="ArrowDown" />
              </el-icon>
            </div>
            
            <el-collapse-transition>
              <div v-show="expandedColleges[college.name]" class="teachers-list">
                <div v-for="teacher in college.teachers" :key="teacher.name" class="teacher-item">
                  <div class="teacher-name">{{ teacher.name }}</div>
                  <div class="teacher-email">{{ teacher.email }}</div>
                </div>
              </div>
            </el-collapse-transition>
          </div>
        </div>
      </el-collapse-transition>
    </el-card>
    
    <!-- 部门联系方式卡片 -->
    <el-card class="departments-card" shadow="hover">
      <div class="card-header" @click="toggleCard('departments')">
        <h3>部门联系方式</h3>
        <el-icon class="expand-icon" :class="{ 'expanded': expandedCards.departments }">
          <component :is="ArrowDown" />
        </el-icon>
      </div>
      
      <el-collapse-transition>
        <div v-show="expandedCards.departments" class="card-content">
          <div v-for="category in departments" :key="category.name" class="department-category">
            <div class="category-header" @click="toggleDepartment(category.name)">
              <h4>{{ category.name }}</h4>
              <el-icon class="expand-icon" :class="{ 'expanded': expandedDepartments[category.name] }">
                <component :is="ArrowDown" />
              </el-icon>
            </div>
            
            <el-collapse-transition>
              <div v-show="expandedDepartments[category.name]" class="department-list">
                <div v-for="dept in category.departments" :key="dept.name" class="department-item">
                  <div class="department-name">{{ dept.name }}</div>
                  <div class="department-contact">{{ dept.contact }}</div>
                </div>
              </div>
            </el-collapse-transition>
          </div>
        </div>
      </el-collapse-transition>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowDown, Search } from '@element-plus/icons-vue'

// 初始数据 - 这里应该从chat.md中提取的实际数据
const colleges = ref([
  {
    name: '商学院',
    teachers: [
      { name: 'José C. Alves 教授', email: 'josealves@cityu.edu.mo' },
      { name: 'José Paulo Afonso Esperança教授', email: 'pauloesperanca@cityu.edu.mo' },
      { name: '田一輝 副教授', email: 'yhtian@cityu.edu.mo' },
      { name: '謝德軍 博士', email: 'djxie@cityu.edu.mo' },
      { name: '趙婧 助理教授', email: 'jingzhao@cityu.edu.mo' },
      { name: '董博文  助理教授', email: 'Bwdong@cityu.edu.mo' },
      { name: 'Dr. Farzad Sabetzadeh', email: 'farzad@cityu.edu.mo' },
      { name: 'Kevin Hannam 博士', email: 'kevinhannam@cityu.edu.mo' },
      { name: '范鴻達 博士', email: 'hontathuam@cityu.edu.mo' },
      { name: '蔡舜  博士', email: 'shuncai@cityu.edu.mo' },
      { name: '黃加順  博士', email: 'jshuang@cityu.edu.mo' },
      { name: '方光怡 博士', email: 'kyfong@cityu.edu.mo' },
      { name: '葛梅 博士', email: 'gemei@cityu.edu.mo' },
      { name: '郭經緯副教授', email: 'jwguo@cityu.edu.mo' },
      { name: '曠婷玥副教授', email: 'kuangtingyue@cityu.edu.mo' },
      { name: '梁靜嫻副教授', email: 'tiffanyleung@cityu.edu.mo' },
      { name: '李卓航 博士', email: 'zhli@cityu.edu.mo' },
      { name: '梁惠雅助理教授', email: 'wnleong@cityu.edu.mo' },
      { name: '黃溢峰助理教授', email: 'yfwong@cityu.edu.mo' },
      { name: '周鳴泉助理教授', email: 'mqzhou@cityu.edu.mo' },
      { name: '左沛鑫助理教授', email: 'pxzuo@cityu.edu.mo' },
      { name: '肖華助理教授', email: 'huaxiao@cityu.edu.mo' },
      { name: '盧亦天助理教授', email: 'ytlu@cityu.edu.mo' },
      { name: '黃一叢助理教授', email: 'ychuang@cityu.edu.mo' },
      { name: '許冰潔助理教授', email: 'bjxu@cityu.edu.mo' },
      { name: '俞凱東助理教授', email: 'kdyu@cityu.edu.mo' },
      { name: '黃柳健 助理教授', email: 'ljhuang@cityu.edu.mo' },
      { name: '馬丹妮 助理教授', email: 'dnma@cityu.edu.mo' },
      { name: '郗迅卓 助理教授', email: 'tomxi@cityu.edu.mo' },
      { name: '逄雪 助理教授', email: 'xuepang@cityu.edu.mo' },
      { name: '邊浩辉 Jose Ferreira Pinto', email: 'josepinto@cityu.edu.mo' },
      { name: '禹俐萌 助理教授', email: 'lmyu@cityu.edu.mo' },
      { name: '趙祖成助理教授', email: 'zczhao@cityu.edu.mo' },
      { name: '李鏡兒 助理教授', email: 'kyeongahlee@cityu.edu.mo' },
      { name: '虞邦幸 助理教授', email: 'bxyu@cityu.edu.mo' },
      { name: '李立夫 助理教授', email: 'lfli@cityu.edu.mo' },
      { name: '張亞峰助理教授', email: 'yfzhang@cityu.edu.mo' },
      { name: '包佳 助理教授', email: 'jiabao@cityu.edu.mo' },
      { name: '張良波助理教授', email: 'liangbozhang@cityu.edu.mo' },
      { name: '梁松聲 Sammy LEUNG', email: 'sammyleung@cityu.edu.mo' },
      { name: '陳為年 博士', email: 'williamchen@cityu.edu.mo' },
      { name: '蔣幸怡', email: 'cathycheong@cityu.edu.mo' },
      { name: 'Wei Wei Seah', email: 'wwseah@cityu.edu.mo' },
      { name: '農真真', email: 'zznong@cityu.edu.mo' },
      { name: '徐沫', email: 'monaxu@cityu.edu.mo' },
      { name: '林泳寧', email: 'christielam@cityu.edu.mo' }
    ]
  },
  {
    name: '数据科学学院',
    teachers: [
      { name: '周万雷 副校长暨数据科学学院院长(兼任)', email: 'wlzhou@cityu.edu.mo' },
      { name: '朱天清教授 副院长', email: 'tqzhu@cityu.edu.mo' },
      { name: '刘文坚副教授 副院长', email: 'andylau@cityu.edu.mo' },
      { name: '朱家伟副教授 课程主任', email: 'cwchu@cityu.edu.mo' },
      { name: '应作斌副教授 课程主任', email: 'zbying@cityu.edu.mo' },
      { name: '郭永德助理教授 课程主任', email: 'wtkuok@cityu.edu.mo' },
      { name: '江恺瑶助理教授 课程主任', email: 'hikong@cityu.edu.mo' },
      { name: '辜嘉 教授', email: 'jiagu@cityu.edu.mo' },
      { name: '孙鑫 教授', email: 'xinsun@cityu.edu.mo' },
      { name: '张宏纲 教授', email: 'hgzhang@cityu.edu.mo' },
      { name: '段俊伟 副教授', email: 'jwduan@cityu.edu.mo' },
      { name: '丁圣勇 特聘教授', email: 'syding@cityu.edu.mo' },
      { name: '吴庚申 助理教授', email: 'gswu@cityu.edu.mo' },
      { name: '葛东娇 助理教授', email: 'djge@cityu.edu.mo' },
      { name: '王淳 助理教授', email: 'chunwang@cityu.edu.mo' },
      { name: '黄志峰 助理教授', email: 'cfwong@cityu.edu.mo' },
      { name: '魏中伦 助理教授', email: 'chunglunwei@cityu.edu.mo' },
      { name: '高万鑫 助理教授', email: 'wanxingao@cityu.edu.mo' },
      { name: '锺婍 助理教授', email: 'qizhong@cityu.edu.mo' },
      { name: '吴晓锋 助理教授', email: 'xiaofengwu@cityu.edu.mo' },
      { name: '崔三帅 助理教授', email: 'sanshuaicui@cityu.edu.mo' },
      { name: '张乐峰 助理教授', email: 'lfzhang@cityu.edu.mo' },
      { name: '罗英喆 助理教授', email: 'yingzheluo@cityu.edu.mo' },
      { name: '敬冯时 助理教授', email: 'fsjing@cityu.edu.mo' },
      { name: '刘驰 助理教授', email: 'chiliu@cityu.edu.mo' },
      { name: '朱聪聪 助理教授', email: 'cczhu@cityu.edu.mo' },
      { name: '张琪 助理教授', email: 'qizhang@cityu.edu.mo' },
      { name: '戚敏锋 助理教授', email: 'mfqi@cityu.edu.mo' },
      { name: '周帅 助理教授', email: 'shuaizhou@cityu.edu.mo' },
      { name: '王铭浩 助理教授', email: 'mhwang@cityu.edu.mo' },
      { name: '李兴风 助理教授', email: 'xfli@cityu.edu.mo' },
      { name: '孙晶 助理教授', email: 'krystalsun@cityu.edu.mo' },
      { name: '孙慧 助理教授', email: 'huisun@cityu.edu.mo' },
      { name: '秦鹏 助理教授', email: 'pengqin@cityu.edu.mo' },
      { name: '钟宇宸 助理教授', email: 'yczhong@cityu.edu.mo' },
      { name: '余蔚 助理教授', email: 'weiyu@cityu.edu.mo' },
      { name: '眭相杰 助理教授', email: 'xjsui@cityu.edu.mo' },
      { name: '谌华杰 助理教授(研究)', email: 'hjchen@cityu.edu.mo' },
      { name: '李正来 助理教授(研究)', email: 'zlli@cityu.edu.mo' },
      { name: '蔡剑平 助理教授(研究)', email: 'jpcai@cityu.edu.mo' },
      { name: '陈昊 助理教授(研究)', email: 'haochen@cityu.edu.mo' },
      { name: '吴世卿 助理教授', email: 'sqwu@cityu.edu.mo' },
      { name: '刘银龙 助理教授', email: 'ylliu@cityu.edu.mo' },
      { name: '陈昶璐 助理教授', email: 'clchen@cityu.edu.mo' },
      { name: '朱泓光 助理教授(研究)', email: 'hgzhu@cityu.edu.mo' },
      { name: '江小凤 讲师', email: 'sfkong@cityu.edu.mo' }
    ]
  },
  {
    name: '金融学院',
    teachers: [
      { name: '张伟光, 教授', email: 'adriancheung@cityu.edu.mo' },
      { name: '邝婉桦, 副教授', email: 'evakhong@cityu.edu.mo' },
      { name: '周泳宏, 教授', email: 'yhzhou@cityu.edu.mo' },
      { name: 'Markus Leibrecht, 教授', email: 'markusleibrecht@cityu.edu.mo' },
      { name: '李强，教授', email: 'qiangli@cityu.edu.mo' },
      { name: '杨挺，副教授', email: 'tingyang@cityu.edu.mo' },
      { name: '林德钦 副教授', email: 'dqlin@cityu.edu.mo' },
      { name: '王应贵 副教授', email: 'ygwang@cityu.edu.mo' },
      { name: '李伟平, 副教授', email: 'wpli@cityu.edu.mo' },
      { name: '娄世艷 副教授', email: 'sylou@cityu.edu.mo' },
      { name: '于博 助理教授', email: 'boyu@cityu.edu.mo' },
      { name: '王方志 助理教授', email: 'fzwang@cityu.edu.mo' },
      { name: '王艳，助理教授', email: 'yanwang@cityu.edu.mo' },
      { name: '白羽，助理教授', email: 'yubai@cityu.edu.mo' },
      { name: '江宇 助理教授', email: 'yujiang@cityu.mo' },
      { name: '李宇鹏, 助理教授', email: 'ypli@cityu.edu.mo' },
      { name: '李迪 助理教授', email: 'dili@cityu.edu.mo' },
      { name: '李蒙, 助理教授', email: 'mengli@cityu.edu.mo' },
      { name: '李乐，助理教授', email: 'leli@cityu.edu.mo' },
      { name: '周尚志，助理教授', email: 'scchow@cityu.edu.mo' },
      { name: '凌云 助理教授', email: 'yunling@cityu.edu.mo' },
      { name: '唐乐文, 助理教授', email: 'lmtong@cityu.edu.mo' },
      { name: '孙晓彤, 助理教授', email: 'xtsun@cityu.edu.mo' },
      { name: '郗健群，助理教授', email: 'jqxi@cityu.edu.mo' },
      { name: '马行舒，助理教授', email: 'xsma@cityu.edu.mo' },
      { name: '高静如，助理教授', email: 'jrgao@cityu.edu.mo' },
      { name: '张岩, 助理教授', email: 'julianzhang@cityu.edu.mo' },
      { name: '许文立，助理教授', email: 'wlxu@cityu.edu.mo' },
      { name: '陈学政，助理教授', email: 'xzchen@cityu.edu.mo' },
      { name: '华君怡，助理教授', email: 'jyhua@cityu.mo' },
      { name: '杨帆，助理教授', email: 'fanyang@cityu.edu.mo' },
      { name: '贾博文, 助理教授', email: 'bwjia@cityu.edu.mo' },
      { name: '赵晶莹 ，助理教授', email: 'jyzhao@cityu.edu.mo' },
      { name: '刘偲，助理教授', email: 'cailiu@cityu.edu.mo' },
      { name: '刘璐, 助理教授', email: 'liulu@cityu.edu.mo' },
      { name: '邓林, 助理教授', email: 'lindeng@cityu.edu.mo' },
      { name: '戴超诺，助理教授', email: 'cndai@cityu.edu.mo' },
      { name: '薛力菲 助理教授', email: 'lfxue@cityu.edu.mo' },
      { name: '庞小川，助理教授', email: 'xcpang@cityu.edu.mo' },
      { name: '梁韫捷，讲师', email: 'kellyliang@cityu.edu.mo' },
      { name: '苏正伟, 讲师', email: 'cwsou@cityu.edu.mo' }
    ]
  },
  {
    name: '人文社科学院',
    teachers: [
      { name: '金立贤 讲座教授 院长', email: 'lixianjin@cityu.edu.mo' },
      { name: '黄国文 教授 副院长', email: 'gwhuang@cityu.edu.mo' },
      { name: '王忠 教授 副院长', email: 'zwang@cityu.edu.mo' },
      { name: '张浩敏 教授 应用语言学研究生课程主任', email: 'hmzhang@cityu.edu.mo' },
      { name: '肖代柏 副教授 文化产业研究生课程主任', email: 'dbxiao@cityu.edu.mo' },
      { name: '徐威 副教授 英语学士及应用语言学学士课程主任', email: 'weixu@cityu.edu.mo' },
      { name: 'Vera Borges 副教授 葡萄牙语学士学位课程主任', email: 'borgesvera@cityu.edu.mo' },
      { name: '沙磊 助理教授 通识教育部课程主任', email: 'shalei@cityu.edu.mo' },
      { name: '陈震 助理教授', email: 'zhenchen@cityu.edu.mo' },
      { name: '侯嘉睿 助理教授', email: 'jiaruihou@cityu.edu.mo' },
      { name: '胡晓 助理教授', email: 'xiaohu@cityu.edu.mo' },
      { name: '黄祥 助理教授', email: 'xianghuang@cityu.edu.mo' },
      { name: '黄婧 助理教授', email: 'jinghuang@cityu.edu.mo' },
      { name: '李筱媛 助理教授', email: 'xiaoyuanli@cityu.edu.mo' },
      { name: '梁伟峻 助理教授', email: 'wjliang@cityu.edu.mo' },
      { name: '刘佳佳 助理教授', email: 'jiajialiu@cityu.edu.mo' },
      { name: '刘彦妗 助理教授', email: 'yjliu@cityu.edu.mo' },
      { name: '邱庄 助理教授', email: 'zhuangqiu@cityu.edu.mo' },
      { name: 'Colum Ruane 助理教授', email: 'columruane@cityu.edu.mo' },
      { name: 'Ekrem Solak 助理教授', email: 'ekremsolak@cityu.edu.mo' },
      { name: '吴宇希 助理教授', email: 'jessiewu@cityu.mo' },
      { name: '张喆 助理教授', email: 'victorzhang@cityu.edu.mo' },
      { name: '周立 助理教授', email: 'lizhou@cityu.edu.mo' },
      { name: '张燕辉 副教授', email: 'yanhuizhang@cityu.edu.mo' },
      { name: 'Sara Augusto 助理教授', email: 'saraaugusto@cityu.edu.mo' },
      { name: 'Pedro Caeiro 助理教授', email: 'pedromiguel@cityu.edu.mo' },
      { name: '林皓晖 讲师', email: 'rafaellam@cityu.edu.mo' },
      { name: 'Romeu Foz 助理教授', email: 'romeufoz@cityu.edu.mo' },
      { name: '刘佳宇 助理教授', email: 'carinaliu@cityu.edu.mo' },
      { name: '隋佳佳 助理教授', email: 'jjsui@cityu.edu.mo' },
      { name: '冯冉 助理教授', email: 'rfeng@cityu.edu.mo' },
      { name: '谢慧铃 副教授', email: 'celinehsieh@cityu.edu.mo' },
      { name: '刘隽敏 助理教授', email: 'junminliu@cityu.edu.mo' },
      { name: '马明 教授', email: 'mingma@cityu.edu.mo' },
      { name: '施瑞婷 助理教授', email: 'rtshi@cityu.edu.mo' },
      { name: '陈岸峰 教授', email: 'nfchan@cityu.edu.mo' },
      { name: '徐倩华 讲师', email: 'annachoi@cityu.edu.mo' },
      { name: '周启亨 讲师', email: 'henrychao@cityu.edu.mo' },
      { name: '何珍 讲师', email: 'chanho@cityu.edu.mo' },
      { name: '李静 副教授', email: 'lijing@cityu.edu.mo' },
      { name: '梅云博 高级讲师', email: 'ybmei@cityu.edu.mo' },
      { name: '彭筱晴 讲师', email: 'laurindapereira@cityu.edu.mo' },
      { name: '陶志威 讲师', email: 'chiwaitou@cityu.edu.mo' },
      { name: '王桂范 讲师', email: 'kfwong@cityu.edu.mo' }
    ]
  },
  {
    name: '大健康学院',
    teachers: [
      { name: '申荷永 教授', email: 'shenheyong@cityu.edu.mo' },
      { name: '孙沛 教授', email: 'peisun@cityu.edu.mo' },
      { name: '王逸雯 助理教授', email: 'tulipswang@cityu.edu.mo' },
      { name: '颖哲华 助理教授', email: 'zhehuaying@cityu.edu.mo' },
      { name: '陈宁轩 助理教授', email: 'nxchen@cityu.edu.mo' },
      { name: '杨红棉 助理教授', email: 'hmyang@cityu.edu.mo' },
      { name: '夏唯伟 助理教授', email: 'weiweixia@cityu.edu.mo' },
      { name: '陆珍妮 讲师', email: 'jennylok@cityu.edu.mo' },
      { name: '郑俊华 讲师', email: 'bencheng@cityu.edu.mo' },
      { name: '杨姝焱 副教授', email: 'syyang@cityu.edu.mo' },
      { name: '胡杰容 助理教授', email: 'jrhu@cityu.edu.mo' },
      { name: '张东航 助理教授', email: 'dhzhang@cityu.edu.mo' },
      { name: '徐雯 助理教授', email: 'wenxu@cityu.edu.mo' },
      { name: '王文津 助理教授', email: 'wjwang@cityu.edu.mo' },
      { name: '葛梅 副教授', email: 'gemei@cityu.edu.mo' },
      { name: '赵亚楠 助理教授', email: 'ynzhao@cityu.edu.mo' },
      { name: '印贇 助理教授', email: 'yunyin@cityu.edu.mo' }
    ]
  },
  {
    name: '创新设计学院',
    teachers: [
      { name: '王伯勛 执行副院长', email: 'phwang@cityu.edu.mo' },
      { name: '周龙 副教授', email: 'lzhou@cityu.edu.mo' },
      { name: '戴定澄 教授', email: '' },
      { name: '韩昊英 教授', email: 'hanhaoying@gmail.com; haoyinghan@cityu.edu.mo' },
      { name: '汪小洋 教授', email: 'xywang@cityu.edu.mo' },
      { name: '邢亚龙 助理教授', email: 'xingyalong@cityu.edu.mo' },
      { name: '谢俊民 副教授', email: 'chunming@cityu.edu.mo' },
      { name: '任玉洁 副教授', email: 'yjren@cityu.edu.mo' },
      { name: '胡欣 助理教授', email: 'xinhu@cityu.edu.mo' },
      { name: '黄广 副教授', email: 'ghuang@cityu.edu.mo' },
      { name: '谢圣明 副教授', email: 'sgxie@cityu.edu.mo' },
      { name: '刘海平 副教授', email: 'hpliu@cityu.edu.mo' },
      { name: '熊磊 副教授', email: 'kmt20005@gmail.com' },
      { name: '李孟顺 高级讲师', email: 'lisalee@cityu.edu.mo' },
      { name: '王俞雅 助理教授', email: 'yywang@cityu.edu.mo' },
      { name: '黎斌 助理教授', email: 'binli@cityu.edu.mo' },
      { name: '杨华杰 助理教授', email: 'yanghj@cityu.edu.mo' },
      { name: '闫宇 助理教授', email: 'yuyan@cityu.edu.mo' },
      { name: '刘婳婳 助理教授', email: 'hhliu@cityu.edu.mo' },
      { name: '闫笑一 助理教授', email: 'xyyan@cityu.edu.mo' },
      { name: '傅宇轩 讲师', email: 'yxfu@cityu.edu.mo' },
      { name: '程情仪 讲师', email: 'nicocheng@cityu.edu.mo' },
      { name: '安舜 助理教授', email: 'shunan@cityu.edu.mo' },
      { name: '赵雨淋 助理教授', email: 'yulinzhao@cityu.edu.mo' },
      { name: '柳婧 助理教授', email: 'jingliu@cityu.edu.mo' },
      { name: '石泓纯 助理教授', email: 'hongchunshi@cityu.edu.mo' },
      { name: '李可润 助理教授', email: 'kerunli@cityu.edu.mo' },
      { name: '李婕 助理教授', email: 'jieli@cityu.edu.mo' },
      { name: '康妮 助理教授', email: 'nikang@cityu.edu.mo' },
      { name: '王子微 助理教授', email: 'zwwang@cityu.edu.mo' },
      { name: '高永杰 助理教授', email: 'yjgao@cityu.edu.mo' },
      { name: '吳家輝 助理教授', email: 'anthony@cityu.mo' },
      { name: '黃駿傑 講師', email: 'kobewong@cityu.mo' },
      { name: '欧阳富', email: 'fuaoIeong@cityu.edu.mo' }
    ]
  },
  {
    name: '国际旅游与管理学院',
    teachers: [
      { name: '李玺 教授、执行副院长(博士生导师)', email: 'xli@cityu.edu.mo' },
      { name: '彭康麟 教授 (博士生导师)', email: 'klpeng@cityu.edu.mo' },
      { name: '范雪丰 教授 (博士生导师)', email: 'xffan@cityu.edu.mo' },
      { name: '沈华文 副教授、博士学位课程主任(博士生导师)', email: 'jamesshen@cityu.edu.mo' },
      { name: '高波 副教授、学士学位课程主任(博士生导师)', email: 'wendygao@cityu.edu.mo' },
      { name: '高玉婷 助理教授、 硕士学位课程主任 (博士生导师)', email: 'estherkou@cityu.edu.mo' },
      { name: '段夏蕾 助理教授 (博士生导师)', email: 'sallyduan@cityu.edu.mo' },
      { name: '吴晓红 助理教授(博士生导师)', email: 'xhwu@cityu.edu.mo' },
      { name: '胡兴报 助理教授(博士生导师)', email: 'simonhu@cityu.edu.mo' },
      { name: '于熙 助理教授(博士生导师)', email: 'xyu@cityu.edu.mo' },
      { name: '林冰娜 助理教授(博士生导师)', email: 'bnlin@cityu.edu.mo' },
      { name: '刘廷瑶 助理教授(博士生导师)', email: 'adrienneliu@cityu.edu.mo' },
      { name: '徐晗 助理教授', email: 'sophiaxu@cityu.edu.mo' },
      { name: '孟婷 助理教授', email: 'tammymeng@cityu.edu.mo' },
      { name: '区伟政 助理教授', email: 'wilsonau@cityu.edu.mo' },
      { name: '薛勛月 助理教授', email: 'joannexue@cityu.edu.mo' },
      { name: '张韵璇 助理教授', email: 'carriezhang@cityu.edu.mo' },
      { name: '游仲恩 助理教授', email: 'joanneyu@cityu.edu.mo' },
      { name: '唐香姐 助理教授', email: 'xjtang@cityu.edu.mo' },
      { name: '张晨曦 助理教授', email: 'cxzhang@cityu.edu.mo' },
      { name: '高明捷 助理教授', email: 'mjgao@cityu.edu.mo' },
      { name: '郭佳楠 助理教授', email: 'jnguo@cityu.edu.mo' },
      { name: '黄利瑶 助理教授', email: 'lyhuang@cityu.edu.mo' },
      { name: '李健文 助理教授', email: 'jwli@cityu.edu.mo' },
      { name: '林柏雨 助理教授', email: 'bylin@cityu.edu.mo' },
      { name: '孙婉婷 助理教授', email: 'wtsun@cityu.edu.mo' },
      { name: '王丹妮 助理教授', email: 'dnwang@cityu.edu.mo' },
      { name: '陈苑仪 助理教授', email: 'yychen@cityu.edu.mo' },
      { name: '罗燕文 高级讲师、课程主任', email: 'janicelaw@cityu.edu.mo' },
      { name: '张涛 高级讲师 (硕士生导师)', email: 'tzhang@cityu.edu.mo' },
      { name: '王盈娟 高级讲师 (博士生导师)', email: 'ycwang@cityu.edu.mo' },
      { name: '何远昌 讲师', email: 'ycho@cityu.edu.mo' },
      { name: '郭人毓 讲师', email: 'ryguo@cityu.edu.mo' },
      { name: '黃學彬教授(博士生導師)', email: 'pku.huang@qq.com' },
      { name: '呂佳穎教授(博士生導師)', email: 'lvjy@zucc.edu.cn' },
      { name: '阮文奇教授(博士生導師)', email: 'wqr1992@163.com' },
      { name: '孔海燕教授(博士生導師)', email: 'konghaiyan@sdu.edu.cn' },
      { name: '王春雷教授(博士生導師)', email: 'wangcl@suibe.edu.cn' },
      { name: '蘇欣慰  教授(碩士生導師)', email: 'suxinwei01@126.com' },
      { name: '蔣慶榮教授  (國際酒店管理課程碩士生導師)', email: '270645046@qq.com' },
      { name: '顧錚教授', email: 'zheng.gu@unlv.edu或z_gu@hotmail.com' },
      { name: '李柏文 教授', email: '309955302@qq.com' },
      { name: '劉松柏教授', email: 'liusb@bnu.edu.cn' },
      { name: '趙金林教授', email: 'zhaoj@fiu.edu' },
      { name: '畢鬥鬥副教授(博士生導師)', email: 'ddbi@scut.edu.cn' },
      { name: '黃猛副教授(博士生導師)', email: '24980049@qq.com' },
      { name: '楊雲副教授(博士生導師)', email: 'yangyunzsu@163.com' },
      { name: '錢建偉 副教授(博士生導師)', email: 'jianweiqian@cityu.mo' },
      { name: '布乃鵬 副教授(博士生導師)', email: 'bunp@sdu.edu.cn' },
      { name: '蘭俊棒 副教授(博士生導師)', email: 'lanjunb@sysu.edu.cn' },
      { name: '劉志鈺 副教授(碩士生導師)', email: '3293805201@qq.com' },
      { name: '吳清 副教授(碩士生導師)', email: 'wuqing599@qq.com' },
      { name: '季靖 副教授(碩士生導師)', email: 'jij@hzcu.edu.cn' },
      { name: '錢莉莉 副教授(碩士生導師)', email: 'qianll@zucc.edu.cn' },
      { name: '王易琦 副教授(碩士生導師)', email: 'yiqi419@hotmail.com' },
      { name: '唐金穩 副教授(碩士生導師)', email: 'tcz0519@163.com' },
      { name: '陳柏如 副教授', email: 'chen.poju@yahoo.com' },
      { name: '陳晨 助理教授(博士生導師)', email: 'chenchenxinzhou@163.com' },
      { name: '房廈 助理教授(博士生導師)', email: 'fangsha@szpt.edu.cn' },
      { name: '吳肇邦 助理教授(博士生導師)', email: 'kennethng@cityu.edu.mo' }
    ]
  },
  {
    name: '教育学院',
    teachers: [
      { name: '程李颖 教授、院长', email: 'liyingcheng@cityu.edu.mo' },
      { name: '陈文锋 教授', email: 'wenfeng118@hotmail.com' },
      { name: '彭俊 副教授 / 博士学位课程主任', email: 'junpeng@cityu.edu.mo' },
      { name: '郑隆威 副教授', email: 'lwzheng@cityu.edu.mo' },
      { name: '代毅 助理教授 / 硕士学位课程主任', email: 'yidai@cityu.edu.mo' },
      { name: '欧阳白晓 助理教授', email: 'claireouyang@cityu.edu.mo' },
      { name: '黄碧云 助理教授', email: 'byhuang@cityu.edu.mo' },
      { name: '张家维 助理教授', email: 'aprilzhang@cityu.edu.mo' },
      { name: '王梓璇 助理教授', email: 'zxwang@cityu.edu.mo' }
    ]
  },
  {
    name: '法学院',
    teachers: [
      { name: '叶桂平 协助副校长、教授', email: 'kpip@cityu.edu.mo' },
      { name: '周平 副教授、硕博导', email: 'pengchao@cityu.edu.mo' },
      { name: '吕冬娟 助理教授、硕博导', email: 'djlyu@cityu.edu.mo' },
      { name: '陈怡 助理教授、硕导', email: 'chenyi@cityu.edu.mo' },
      { name: '何琪 助理教授、硕导', email: 'qihe@cityu.edu.mo' },
      { name: '范雪珂 助理教授、硕导', email: 'xkfan@cityu.edu.mo' },
      { name: '冯彦龙 博士', email: 'ivan5v11ivan107@hotmail.com' },
      { name: '张雪莲 博士', email: 'lilycheong@cityu.mo' }
    ]
  },
  {
    name: '葡语学院',
    teachers: [
      { name: '叶桂平 院长、教授', email: 'kpip@cityu.edu.mo' },
      { name: '周平 副教授', email: 'pengchao@cityu.edu.mo' },
      { name: '柳嘉信 副教授', email: 'chleou@cityu.edu.mo' },
      { name: 'João Simões 主任', email: 'joaosimoes@cityu.edu.mo' },
      { name: '陈红 副教授', email: 'hongchen@cityu.edu.mo' },
      { name: '施养正 助理教授', email: 'icsi@cityu.edu.mo' },
      { name: '周佳圆 讲师', email: 'Jiayuanzhou@cityu.edu.mo' },
      { name: '葛思宁 讲师', email: 'siningge@cityu.edu.mo' },
      { name: '劉洪鐘', email: 'hongzhongliu@126.com' },
      { name: '张敏', email: 'zhangmin@cass.org.cn' },
      { name: '潘燈', email: 'pandeng@vip.sina.com' },
      { name: '周志伟', email: 'zhouzw@cass.org.cn' }
    ]
  }
])

// 部门联系方式数据
const departments = ref([
  {
    name: '行政部门',
    departments: [
      { name: '教务处', contact: '教务处联系方式' },
      { name: '学生事务处', contact: '学生事务处联系方式' },
      { name: '图书馆', contact: '图书馆联系方式' },
      { name: '信息技术服务中心', contact: '信息技术服务中心联系方式' },
      { name: '宿舍管理处', contact: '宿舍管理处联系方式' }
    ]
  },
  {
    name: '学院',
    departments: [
      { name: '商学院', contact: '商学院联系方式' },
      { name: '数据科学学院', contact: '数据科学学院联系方式' },
      { name: '金融学院', contact: '金融学院联系方式' },
      { name: '人文社科学院', contact: '人文社科学院联系方式' },
      { name: '大健康学院', contact: '大健康学院联系方式' },
      { name: '创新设计学院', contact: '学院電郵：fiad@cityu.edu.mo, 学院网址：https://fiad.cityu.edu.mo' },
      { name: '国际旅游与管理学院', contact: '国际旅游与管理学院联系方式' },
      { name: '教育学院', contact: '教育学院联系方式' },
      { name: '法学院', contact: '法学院联系方式' },
      { name: '葡语学院', contact: '葡语学院联系方式' }
    ]
  }
])

// 展开状态
const expandedCards = ref({
  search: true,
  teachers: true,
  departments: true
})

const expandedColleges = ref({})
const expandedDepartments = ref({})

// 搜索相关
const searchKeyword = ref('')
const searchResults = computed(() => {
  if (!searchKeyword.value.trim()) return []
  
  const keyword = searchKeyword.value.toLowerCase()
  const results = []
  
  // 搜索教师
  colleges.value.forEach(college => {
    college.teachers.forEach(teacher => {
      if (
        teacher.name.toLowerCase().includes(keyword) ||
        teacher.email.toLowerCase().includes(keyword) ||
        college.name.toLowerCase().includes(keyword)
      ) {
        results.push({
          id: `${college.name}-${teacher.name}`,
          type: '教师',
          name: teacher.name,
          contact: teacher.email,
          department: college.name
        })
      }
    })
  })
  
  // 搜索部门
  departments.value.forEach(category => {
    category.departments.forEach(dept => {
      if (
        dept.name.toLowerCase().includes(keyword) ||
        dept.contact.toLowerCase().includes(keyword)
      ) {
        results.push({
          id: `${category.name}-${dept.name}`,
          type: '部门',
          name: dept.name,
          contact: dept.contact,
          department: category.name
        })
      }
    })
  })
  
  return results
})

// 切换卡片展开状态
const toggleCard = (cardType) => {
  expandedCards.value[cardType] = !expandedCards.value[cardType]
}

// 切换学院展开状态
const toggleCollege = (collegeName) => {
  expandedColleges.value[collegeName] = !expandedColleges.value[collegeName]
}

// 切换部门展开状态
const toggleDepartment = (deptName) => {
  expandedDepartments.value[deptName] = !expandedDepartments.value[deptName]
}

// 初始化所有学院和部门为展开状态
colleges.value.forEach(college => {
  expandedColleges.value[college.name] = true
})

departments.value.forEach(dept => {
  expandedDepartments.value[dept.name] = true
})
</script>

<style scoped>
.contacts-container {
  padding: 30px;
  background: #f5f5f5;
  min-height: calc(100vh - 60px);
}

.contacts-container h2 {
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.search-card, .teachers-card, .departments-card {
  margin-bottom: 20px;
  border-left: 4px solid #409eff;
  transition: all 0.3s;
}

.search-card:hover, .teachers-card:hover, .departments-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
  transform: translateY(-2px);
}

.card-header, .search-header {
  width: 100%;
  cursor: pointer;
  padding: 12px 16px;
  margin: -4px;
  border-radius: 4px;
  transition: background-color 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header:hover, .search-header:hover {
  background-color: #f5f7fa;
}

.card-header h3, .search-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

.expand-icon {
  transition: transform 0.3s;
  color: #909399;
  font-size: 18px;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

.search-content {
  padding: 16px 0;
}

.search-content .el-input {
  margin-bottom: 16px;
}

.search-results {
  max-height: 400px;
  overflow-y: auto;
}

.search-result-item {
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 8px;
  background: #fafafa;
}

.result-type {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.result-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.result-contact {
  color: #606266;
  font-size: 14px;
  margin-bottom: 4px;
}

.result-department {
  font-size: 12px;
  color: #909399;
}

.card-content {
  padding: 16px 0;
}

.college-section, .department-category {
  margin-bottom: 16px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background: #fff;
}

.college-header, .category-header {
  padding: 12px 16px;
  background: #f5f7fa;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ebeef5;
}

.college-header:hover, .category-header:hover {
  background: #eee;
}

.college-header h4, .category-header h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.teachers-list, .department-list {
  padding: 12px;
}

.teacher-item, .department-item {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
}

.teacher-item:last-child, .department-item:last-child {
  border-bottom: none;
}

.teacher-name, .department-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.teacher-email, .department-contact {
  color: #606266;
  font-size: 14px;
}
</style>