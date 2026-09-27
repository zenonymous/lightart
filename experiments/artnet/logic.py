import asyncio

async def breathe(intensity,step):
	print(f"begin breathe -> step is nu {step}")
	stap = step / 8 
	print(f"===> stap is nu {stap}")
	if stap % 2 == 0:
		print ("check, adem in")
	else:
		print ("check, adem uit")


for step in range (0,48,8):
	print(f"op het punt breathe aan te roepen en step is nu {step}")
	asyncio.run(breathe(255,step))
