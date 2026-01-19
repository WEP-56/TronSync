"""
Flask后端API服务
提供RESTful接口供前端调用
"""
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import logging
import traceback

from api.course_api import CourseAPI
from api.schedule_api import ScheduleAPI
from api.announcement_api import AnnouncementAPI
from api.user_api import UserAPI
from api.file_api import FileAPI
from core.session_manager import SessionManager
from core import config_manager
from core.updater import Updater
import threading
import os
import time

# 应用版本号
APP_VERSION = "v1.0.0"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
app.secret_key = 'your-secret-key-change-this'  # 用于session管理
CORS(app, supports_credentials=True)  # 允许跨域，支持cookie

# 全局session管理器
session_manager = SessionManager()


@app.route('/')
def index():
    """返回前端页面"""
    return app.send_static_file('index.html')


@app.route('/favicon.ico')
def favicon():
    """返回 favicon（如果不存在则返回 204）"""
    try:
        return app.send_static_file('favicon.ico')
    except:
        return '', 204


@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
        
        logger.info(f"尝试登录: {username}")
        
        # 调用SessionManager登录
        success = session_manager.login(username, password)
        
        if success:
            # 保存登录状态到Flask session
            session['logged_in'] = True
            session['username'] = username
            
            # 获取用户信息
            user_api = UserAPI(session_manager.get_session())
            user_profile = user_api.get_profile()
            
            logger.info(f"✅ 登录成功: {username}")
            return jsonify({
                'success': True,
                'message': '登录成功',
                'user': {
                    'name': user_profile.name_cn if user_profile else username,
                    'student_id': user_profile.account if user_profile else '',
                    'email': user_profile.email if user_profile else ''
                }
            })
        else:
            logger.warning(f"❌ 登录失败: {username}")
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
            
    except Exception as e:
        logger.error(f"登录异常: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'登录失败: {str(e)}'}), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    session_manager.clear_session()
    return jsonify({'success': True, 'message': '登出成功'})


@app.route('/api/courses', methods=['GET'])
def get_courses():
    """获取课程列表"""
    try:
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': '未登录'}), 401
        
        logger.info("获取课程列表")
        course_api = CourseAPI(session_manager.get_session())
        courses = course_api.get_courses()
        
        # 转换为字典列表
        courses_data = []
        for course in courses:
            courses_data.append({
                'id': course.course_id,  # 注意是course_id不是id
                'name': course.name,
                'code': course.course_code,  # 注意是course_code不是code
                'teacher': ', '.join(course.instructors) if course.instructors else '',  # 教师是列表
                'credits': course.credit,  # 注意是credit不是credits
                'semester': course.semester,
                'description': ''  # Course模型没有description字段
            })
        
        logger.info(f"✅ 获取到 {len(courses_data)} 门课程")
        return jsonify({'success': True, 'data': courses_data})
        
    except Exception as e:
        logger.error(f"获取课程列表异常: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'获取失败: {str(e)}'}), 500


@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    """获取公告列表"""
    try:
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': '未登录'}), 401
        
        logger.info("获取公告列表")
        announcement_api = AnnouncementAPI(session_manager.get_session())
        announcements = announcement_api.get_bulletins()  # 注意方法名是get_bulletins
        
        # 转换为字典列表
        announcements_data = []
        for announcement in announcements:
            announcements_data.append({
                'id': announcement.id if hasattr(announcement, 'id') else '',
                'title': announcement.title,
                'content': announcement.content,
                'publish_time': announcement.created_at,  # 注意字段名是created_at
                'course_name': announcement.course_name
            })
        
        logger.info(f"✅ 获取到 {len(announcements_data)} 条公告")
        return jsonify({'success': True, 'data': announcements_data})
        
    except Exception as e:
        logger.error(f"获取公告列表异常: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'获取失败: {str(e)}'}), 500


@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    """获取课程表"""
    try:
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': '未登录'}), 401
        
        logger.info("获取课程表")
        schedule_api = ScheduleAPI(session_manager.get_session())
        schedule = schedule_api.get_schedule()
        
        if not schedule:
            return jsonify({'success': False, 'message': '获取课程表失败'}), 500
        
        # 转换为字典
        schedules_data = []
        for course_schedule in schedule.schedules:
            schedules_data.append({
                'course_name': course_schedule.course_name,
                'teacher': course_schedule.teacher,
                'classroom': course_schedule.classroom,
                'week_day': course_schedule.week_day,
                'start_time': course_schedule.start_time,
                'end_time': course_schedule.end_time,
                'start_section': course_schedule.start_section,
                'end_section': course_schedule.end_section,
                'weeks': course_schedule.weeks,
                'course_type': course_schedule.course_type,
                'credits': course_schedule.credits
            })
        
        logger.info(f"✅ 获取到 {len(schedules_data)} 节课程")
        return jsonify({
            'success': True,
            'data': {
                'week_number': schedule.week_number,
                'schedules': schedules_data
            }
        })
        
    except Exception as e:
        logger.error(f"获取课程表异常: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'获取失败: {str(e)}'}), 500


@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """获取用户信息"""
    try:
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': '未登录'}), 401
        
        logger.info("获取用户信息")
        user_api = UserAPI(session_manager.get_session())
        user_profile = user_api.get_profile()
        
        if user_profile:
            return jsonify({
                'success': True,
                'data': {
                    'name': user_profile.name_cn or '',
                    'student_id': user_profile.account or '',
                    'email': user_profile.email or '',
                    'major': user_profile.program or '',
                    'avatar_url': user_profile.avatar_url or '',
                    'platform_role': user_profile.platform_role or ''
                }
            })
        else:
            return jsonify({'success': False, 'message': '获取用户信息失败'}), 500
            
    except Exception as e:
        logger.error(f"获取用户信息异常: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'获取失败: {str(e)}'}), 500


@app.route('/api/files', methods=['GET'])
def get_files():
    """获取文件列表"""
    try:
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': '未登录'}), 401
        
        logger.info("获取文件列表")
        file_api = FileAPI(session_manager.get_session())
        
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        parent_id = int(request.args.get('parent_id', 0))
        
        result = file_api.get_files(page=page, page_size=page_size, parent_id=parent_id)
        
        # 统计文件和文件夹数量
        folders_count = sum(1 for f in result['files'] if f['type'] == 'folder')
        files_count = len(result['files']) - folders_count
        
        logger.info(f"✅ 获取到 {len(result['files'])} 个项目 ({folders_count} 个文件夹, {files_count} 个文件)")
        return jsonify({
            'success': True,
            'data': result['files'],
            'breadcrumb': result['breadcrumb'],
            'parent_id': result['parent_id'],
            'pagination': {
                'page': result['page'],
                'page_size': page_size,
                'total': result['total'],
                'pages': result['pages']
            }
        })
        
    except Exception as e:
        logger.error(f"获取文件列表异常: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'获取失败: {str(e)}'}), 500


@app.route('/api/check-login', methods=['GET'])
def check_login():
    """检查登录状态"""
    if session.get('logged_in'):
        return jsonify({'success': True, 'logged_in': True, 'username': session.get('username')})
    else:
        return jsonify({'success': True, 'logged_in': False})


@app.route('/api/config/credentials', methods=['GET'])
def get_credentials():
    """获取保存的登录凭证"""
    try:
        config = config_manager.load_config()
        return jsonify({
            'success': True,
            'data': {
                'username': config.get('username', ''),
                'password': config.get('password', ''),
                'remember_password': config.get('remember_password', False),
                'auto_login': config.get('auto_login', False)
            }
        })
    except Exception as e:
        logger.error(f"获取凭证失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/config/credentials', methods=['POST'])
def save_credentials():
    """保存登录凭证"""
    try:
        data = request.get_json()
        config = config_manager.load_config()
        
        if data.get('remember_password'):
            config['username'] = data.get('username', '')
            config['password'] = data.get('password', '')
            config['remember_password'] = True
            config['auto_login'] = data.get('auto_login', False)
        else:
            # 不保存密码，清除凭证
            config.pop('username', None)
            config.pop('password', None)
            config['remember_password'] = False
            config['auto_login'] = False
        
        config_manager.save_config(config)
        return jsonify({'success': True, 'message': '保存成功'})
    except Exception as e:
        logger.error(f"保存凭证失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/config/settings', methods=['GET'])
def get_settings():
    """获取设置"""
    try:
        config = config_manager.load_config()
        settings = config.get('settings', {
            'theme': 'light',
            'compactMode': False,
            'downloadPath': '',
            'autoRefreshInterval': 5,
            'autoLogin': config.get('auto_login', False),
            'notifyNewAnnouncement': True,
            'notifyCourse': False
        })
        return jsonify({'success': True, 'data': settings})
    except Exception as e:
        logger.error(f"获取设置失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/config/settings', methods=['POST'])
def save_settings():
    """保存设置"""
    try:
        data = request.get_json()
        config = config_manager.load_config()
        config['settings'] = data
        
        # 同步自动登录设置
        if 'autoLogin' in data:
            config['auto_login'] = data['autoLogin']
        
        config_manager.save_config(config)
        return jsonify({'success': True, 'message': '保存成功'})
    except Exception as e:
        logger.error(f"保存设置失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/system/select-folder', methods=['POST'])
def select_folder():
    """选择文件夹（用于设置下载路径）"""
    try:
        # 这个功能需要 pywebview 支持
        # 返回一个占位符，实际实现需要在 run.py 中通过 pywebview API 实现
        return jsonify({
            'success': True,
            'path': '',
            'message': '文件夹选择功能需要在桌面应用中实现'
        })
    except Exception as e:
        logger.error(f"选择文件夹失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/files/download', methods=['POST'])
def download_file_api():
    """下载文件到本地"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        file_name = data.get('file_name')
        
        if not file_id:
            return jsonify({'success': False, 'message': '文件ID不能为空'}), 400
        
        # 获取下载路径
        config = config_manager.load_config()
        download_path = config.get('settings', {}).get('downloadPath', '')
        
        # 构造文件下载URL
        download_url = f"https://tronclass.cityu.edu.mo/api/uploads/{file_id}/blob"
        
        # 使用 session 下载文件
        file_api = FileAPI(session_manager.get_session())
        response = file_api.session.get(download_url, stream=True, timeout=30)
        
        if response.status_code == 200:
            # 确定保存路径
            import os
            if download_path and os.path.exists(download_path):
                save_path = os.path.join(download_path, file_name)
            else:
                # 使用默认下载路径
                save_path = os.path.join(os.path.expanduser('~'), 'Downloads', file_name)
            
            # 保存文件
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"✅ 文件下载成功: {save_path}")
            return jsonify({
                'success': True,
                'message': '下载成功',
                'path': save_path
            })
        else:
            logger.error(f"下载文件失败，状态码: {response.status_code}")
            return jsonify({'success': False, 'message': '下载失败'}), 500
            
    except Exception as e:
        logger.error(f"下载文件异常: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'下载失败: {str(e)}'}), 500


@app.route('/api/system/check-update', methods=['GET'])
def check_update():
    """检查更新"""
    try:
        updater = Updater(APP_VERSION)
        result = updater.check_for_updates()
        return jsonify(result)
    except Exception as e:
        logger.error(f"检查更新接口异常: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/perform-update', methods=['POST'])
def perform_update():
    """执行更新"""
    try:
        data = request.json
        download_url = data.get('download_url')
        if not download_url:
            return jsonify({'success': False, 'message': 'Missing download_url'}), 400
        
        def update_task():
            updater = Updater(APP_VERSION)
            result = updater.perform_update(download_url)
            if result.get('success'):
                logger.info("更新准备就绪，即将退出程序...")
                time.sleep(1) # 给前端一点时间接收响应
                os._exit(0) # 强制退出，由 update.bat 接管
            else:
                logger.error(f"更新失败: {result.get('message')}")

        # 在后台线程执行更新，避免阻塞请求
        thread = threading.Thread(target=update_task)
        thread.start()
        
        return jsonify({'success': True, 'message': '更新下载已在后台开始，下载完成后应用将自动重启'})
            
    except Exception as e:
        logger.error(f"执行更新接口异常: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
