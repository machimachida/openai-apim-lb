import os
import time
import asyncio
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

load_dotenv()

apim_endpoint = os.getenv("APIM_ENDPOINT")
apim_subscription_key = os.getenv("APIM_SUBSCRIPTION_KEY")

# リクエストの総数
TOTAL_REQUESTS = 43

# 非同期クライアントの作成
async_client = AsyncAzureOpenAI(
    azure_endpoint=apim_endpoint,  # do not add "/openai" at the end here because this will be automatically added by this SDK
    api_key=apim_subscription_key,
    api_version="2023-12-01-preview"
)

# 単一リクエスト用の関数
async def make_request(request_id):
    try:
        start_time = time.time()
        response = await async_client.chat.completions.create(
            model="chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Request {request_id}: Does Azure OpenAI support customer managed keys?"}
            ]
        )
        end_time = time.time()
        print(f"Request {request_id} completed in {end_time - start_time:.2f} seconds")
        return response
    except Exception as e:
        print(f"Request {request_id} failed: {e}")
        return None

# メイン関数
async def main():
    print(f"Starting {TOTAL_REQUESTS} parallel requests...")
    start_time = time.time()
    
    # 複数のリクエストを非同期で実行
    tasks = [make_request(i) for i in range(1, TOTAL_REQUESTS + 1)]
    responses = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    # 成功した応答の数を数える
    successful_responses = sum(1 for resp in responses if resp is not None)
    
    print(f"\nCompleted {successful_responses} out of {TOTAL_REQUESTS} requests")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    
    # サンプルとして、最初の成功した応答を表示
    for response in responses:
        if response is not None:
            print("\nSample response content:")
            print(response.choices[0].message.content)
            break

# スクリプトが直接実行されたときに実行
if __name__ == "__main__":
    asyncio.run(main())