import re
import os

def classify_and_extract_ips(input_filename='all.txt'):
    """
    读取文件，排除注释行，并将地址分为 IPv4/IPv4 CIDR/IPv6/IPv6 CIDR 四类，
    分别保存到四个不同的文件中。
    """
    results = {
        'ipv4_addresses': [],
        'ipv4_cidr': [],
        'ipv6_addresses': [],
        'ipv6_cidr': [],
    }

    # IPv4 地址和 CIDR 匹配 (排除注释后，仅匹配非注释行)
    ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b')

    # IPv6 地址和 CIDR 匹配 (修正后的，用于确保捕获子网掩码)
    ipv6_pattern = re.compile(r'\b(?:[0-9a-fA-F]*:){2,}[0-9a-fA-F:.]*(?:/\d{1,3})?')
    
    if not os.path.exists(input_filename):
        print(f"错误：输入文件 '{input_filename}' 未找到。")
        return

    try:
        with open(input_filename, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith('#'):
                    continue

                # 分类 IPv4
                ipv4_matches = ipv4_pattern.findall(stripped_line)
                for match in ipv4_matches:
                    if '/' in match:
                        results['ipv4_cidr'].append(match)
                    else:
                        results['ipv4_addresses'].append(match)
                        
                # 分类 IPv6
                ipv6_matches = ipv6_pattern.findall(stripped_line)
                for match in ipv6_matches:
                    if '/' in match:
                        results['ipv6_cidr'].append(match)
                    else:
                        results['ipv6_addresses'].append(match)

        # 写入四个输出文件
        output_files = {
            'ipv4_addresses': 'ipv4_addresses_only.txt',
            'ipv4_cidr': 'ipv4_cidr_only.txt',
            'ipv6_addresses': 'ipv6_addresses_only.txt',
            'ipv6_cidr': 'ipv6_cidr_only.txt',
        }

        for key, filename in output_files.items():
            if results[key]:
                # 去重并写入文件
                unique_addresses = list(dict.fromkeys(results[key]))
                with open(filename, 'w', encoding='utf-8') as f_out:
                    for address in unique_addresses:
                        f_out.write(address + '\n')
            else:
                # 确保文件存在，即使内容为空
                open(filename, 'w').close() 
        
        print("所有地址分类和提取完成。")

    except Exception as e:
        print(f"处理文件时发生错误: {e}")

if __name__ == "__main__":
    classify_and_extract_ips()
