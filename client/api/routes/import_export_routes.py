from flask import Blueprint, request, jsonify, send_file
from services.import_export_service import ImportExportService
import tempfile
import os
import yaml

bp = Blueprint('import_export', __name__)

# 加载配置
def load_config():
    # 获取项目根目录
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_path = os.path.join(root_dir, 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()
import_export_service = ImportExportService(db_path=config['database']['path'])

@bp.route('/export/json', methods=['GET'])
def export_json():
    """导出任务为JSON文件"""
    try:
        json_data = import_export_service.export_tasks_to_json()
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            f.write(json_data)
            temp_path = f.name
        
        return send_file(
            temp_path,
            mimetype='application/json',
            as_attachment=True,
            download_name='tasks.json'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 清理临时文件
        if 'temp_path' in locals():
            os.unlink(temp_path)

@bp.route('/export/csv', methods=['GET'])
def export_csv():
    """导出任务为CSV文件"""
    try:
        csv_data = import_export_service.export_tasks_to_csv()
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        return send_file(
            temp_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='tasks.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 清理临时文件
        if 'temp_path' in locals():
            os.unlink(temp_path)

@bp.route('/import/json', methods=['POST'])
def import_json():
    """从JSON文件导入任务"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '未上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '未选择文件'}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({'error': '文件格式必须是JSON'}), 400
        
        json_data = file.read().decode('utf-8')
        results = import_export_service.import_tasks_from_json(json_data)
        
        return jsonify({
            'message': f'成功导入 {len(results)} 个任务',
            'tasks': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/import/csv', methods=['POST'])
def import_csv():
    """从CSV文件导入任务"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '未上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '未选择文件'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': '文件格式必须是CSV'}), 400
        
        csv_data = file.read().decode('utf-8')
        results = import_export_service.import_tasks_from_csv(csv_data)
        
        return jsonify({
            'message': f'成功导入 {len(results)} 个任务',
            'tasks': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 