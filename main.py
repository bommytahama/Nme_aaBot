import discord
from discord.ext import commands
import os
import anim
import ffmpeg
import random
import re

client = commands.Bot(intents=discord.Intents.all(), command_prefix='?')

class mock_comm:
  def __init__(self, username: str, text: str, score: int = 0):
        self.author = username
        self.body = text
        self.score = score

@client.event
async def on_ready():
  print('ready')
  #channel = client.get_channel(725245718750822411)
  #mes = await channel.fetch_message(812065298622447658)
  #mes2 = await channel.fetch_message(812068473152864256)
  #print(mes.content)
  #print(mes2.content)

def compress_video(video_full_path, output_file_name, target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()

def check_for_link(text):
  counter = 0
  na = ['http', '.com', '.gif']
  for end in na:
    if end in text:
      counter += 1
  if counter > 0:
    return True
  else:
    return False

def ran_let(length):
  alpha = {
    '1': 'a',
    '2': 'b',
    '3': 'c',
    '4': 'd',
    '5': 'e',
    '6': 'f',
    '7': 'g',
    '8': 'h',
    '9': 'i',
    '10': 'j',
    '11': 'k',
    '12': 'l',
    '13': 'm',
    '14': 'n',
    '15': 'o',
    '16': 'p',
    '17': 'q',
    '18': 'r',
    '19': 's',
    '20': 't',
    '21': 'u',
    '22': 'v',
    '23': 'w',
    '24': 'x',
    '25': 'y',
    '26': 'z',
  }

  rstr = ""
  for i in range(length):
    rstr += alpha[str(random.randint(1, 26))]
  return rstr
    
def mention_stuff(mes_list, cx):
  rlist = []
  for mes in mes_list:
    thing = mes.content
    if mes.mentions:
      m = re.search('<(.+?)>', thing)
      while m:
        u_id = int(m.group(1).replace('@!', ''))
        memb = cx.guild.get_member(u_id)
        name = str(memb.name)
        thing = thing.replace('<@!' + str(memb.id) + '>', '@' + name)
        m = re.search('<(.+?)>', thing)
    rlist.append([str(mes.author.name), thing]) 
  return rlist

async def upcount_ids(afterm, beforem, cx):      
    channel = beforem.channel

    hlist0 = await channel.history(limit=80, around=afterm, oldest_first=True).flatten()
    hlist = await channel.history(limit=19, before=beforem, after=afterm).flatten()
    
    hlist.insert(0, afterm)
    hlist.append(hlist0[hlist0.index(hlist[-1]) + 1])

    for item in hlist:
      if not(len(item.content) > 0) or check_for_link(item.content.lower()):
        hlist.remove(item)
    
    return_list = mention_stuff(hlist, cx)
    return return_list

async def upcount(num, skip, cx):
  channel = cx.channel
  lim = 70
  hlist = await channel.history(limit=lim).flatten()
  print(len(hlist))
  n = int(num)
  #print(f'num is {n}')
  counter = int(skip)
  hlist2 = []
  hlist.pop(0)
  hlist.pop(0)
  while n > 0 and counter < lim - 2:
    #print(str(counter))
    #print(str(n))
    if len(hlist[counter].content) > 0 and not(check_for_link(hlist[counter].content.lower())):
      hlist2.insert(0, hlist[counter])
      n -= 1
      #print('counter is ' + str(counter))
      print(str(n))
    counter += 1

  return_list = mention_stuff(hlist2, cx)
  return return_list



def stuff(mes1_list=[
    ['dhnwjakdwa', 'this is a video'],
    ['dhwwhjakwa', 'FUCK'],
    ]):

    mes_list = []
    mes_list2 = []
    for mes1 in mes1_list:
      print(mes1)
      obj = mock_comm(mes1[0], mes1[1])
      mes_list.append(obj)
      mes_list2.append(obj)


    def mes_name_sort(mes_obj_list):
        mfd = {}
        for mes in mes_obj_list:
          try:
            mfd[str(mes.author)] += 1
          except KeyError:
            mfd[str(mes.author)] = 1
        mfdl = list(mfd)

        f_l = []
        for i in mfdl:
          f_l.append(mfd[i])

        sorted_names = []
        what = []
        for i in f_l:
          what.append(i)

        mol_s = []
        for i in what:
          #print(f_l_n)
          maxx = max(f_l)
          maxx_l = f_l.index(maxx)
          sorted_names.append(mfdl[maxx_l])
          mol_s.append(mes_obj_list[maxx_l])
          del mes_obj_list[maxx_l]
          del f_l[maxx_l]
          del mfdl[maxx_l]
        return sorted_names

    sn = mes_name_sort(mes_list)

    #print(mes_list2)
 
    #print(mes_list2)
    print('getting charcaters')
    characters = anim.get_characters(sn)
    print('got characters, getting scene')
    anim.comments_to_scene(mes_list2, characters, output_filename='hello.mp4')
    print('got scene')
    compress_video('hello.mp4', 'video.mp4', 5500)

async def send_vid(cx):
    await cx.channel.send(file=discord.File('video.mp4'))

    files_to_remove = ['hello.mp4', 'test.mp4', 'final_se.mp3', 'video.mp4', 'ffmpeg2pass-0.log', 'ffmpeg2pass-0.log.mbtree']
    for f in files_to_remove:
      os.remove(f)
      
    print('done')

@client.command(
  help='does something',
  brief='fuck you'
)
async def aa(ctx, *args):
    args2 = list(args)
    try: 
      count_up = int(args2[0])
      skip = int(args2[1])
    except IndexError:
      await ctx.channel.send('input 2 numbers dummy')
      return
    
    if count_up > 30:
      await ctx.channel.send('too many messages (try something less than 30)')
      return
    
    if count_up + skip > 67:
      await ctx.channel.send('too many messages!!!!!!!!!!!')
      return
    
    await ctx.channel.send(ran_let(random.randint(10, 30)) + ' makijg vdieo')
    stuff(await upcount(count_up, skip, ctx))

    await send_vid(ctx)


@client.command(
  help='does something',
  brief='fuck you'
)
async def aa_id(ctx, *args):
    args2 = list(args)

    channel = ctx.channel
    try:
      after = args2[0]
      before = args2[1]
    except IndexError:
      await ctx.channel.send('input 2 ids dummy')
      return
    
    try:
      afterm = await channel.fetch_message(int(after))
      beforem = await channel.fetch_message(int(before))
    except discord.NotFound:
      await channel.send('one or more ids is/are not valid')
      return
    
    await ctx.channel.send(ran_let(random.randint(10, 30)) + ' makijg vdieo')
    stuff(await upcount_ids(afterm, beforem, ctx))

    await send_vid(ctx)

    
#client.run(os.getenv('TOKEN'))