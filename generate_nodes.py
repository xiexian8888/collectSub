#https://github.com/mariahlamb/proxy-sub
import os
import requests
import base64

def extract_nodes(text):
    """
    过滤并提取有效的节点信息
    支持Base64编码和普通文本的节点
    """
    valid_node_prefixes = ['ss://', 'ssr://', 'vmess://', 'vless://', 'trojan://', 'hysteria://']
    nodes = []
    
    # 尝试解码Base64编码的订阅内容
    try:
        decoded_text = base64.b64decode(text).decode('utf-8')
        lines = decoded_text.split('\n')
    except:
        lines = text.split('\n')
    
    # 筛选有效节点
    for line in lines:
        line = line.strip()
        if any(line.startswith(prefix) for prefix in valid_node_prefixes):
            nodes.append(line)
    
    return nodes

# 文件路径
sub_folder = 'sub'
sub_file = os.path.join(sub_folder, 'sub_all_clash.txt')
output_file = 'all_nodes.txt'

if os.path.exists(sub_file):
    with open(sub_file, 'r') as f:
        subscriptions = f.readlines()
    
    with open(output_file, 'w') as out_f:
        for url in subscriptions:
            url = url.strip()
            if url:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    # 提取并写入有效节点
                    nodes = extract_nodes(response.text.strip())
                    for node in nodes:
                        out_f.write(f'{node}\n')
                        
                except requests.RequestException as e:
                    print(f'获取 {url} 失败: {e}')
    
    print(f'节点信息已更新到：{output_file}')
else:
    print(f'未找到 {sub_file} 文件，跳过生成步骤。')
