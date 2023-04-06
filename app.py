from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # 解析报警消息
    data = request.get_json()
    print(data)
    for alert in data.get('alerts', []):
        # 获取报警级别、摘要和详情
        severity = alert['labels'].get('severity', 'unknown')
        summary = alert['annotations'].get('summary', 'unknown')
        description = alert['annotations'].get('description', 'unknown')
        message = f'[{severity.upper()}] {summary}: {description}'

        # 发送到飞书
        feishu_token = '937763a3-95e5-4bcb-bfaa-ef3d32256409'
        webhook_feishu_url = f'https://open.feishu.cn/open-apis/bot/v2/hook/{feishu_token}'
        message_data_feishu = {
          "msg_type": "text",
          "content": {
            "text": message
          }
        }
        # response = requests.post(webhook_feishu_url, json=message_data_feishu)
        # if response.status_code != 200:
        #     print(f'Failed to send notification to FeiShu Work: {response.text}')


        # 发送通知到企业微信
        # webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key'
        # corpid = 'your-corporation-id'
        # corpsecret = 'your-corporation-secret'
        # agentid = 'your-agent-id'
        # access_token_url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}'
        # response = requests.get(access_token_url)
        # access_token = response.json().get('access_token', '')
        # message_data = {
        #     'msgtype': 'text',
        #     'agentid': agentid,
        #     'text': {
        #         'content': message,
        #     },
        # }
        # response = requests.post(webhook_url + f'&access_token={access_token}', json=message_data)
        # if response.status_code != 200:
        #     print(f'Failed to send notification to WeChat Work: {response.text}')

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
