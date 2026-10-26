"""Rebuild the three figures used by reports/2026-10-27/0135-report.md.

Restored from this chat's original drawing code. See README.md for sources,
dependencies, font requirements, and the reproduction check.
"""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
OUT = args.output_dir.resolve()
OUT.mkdir(parents=True, exist_ok=True)
FONT = 'C:/Windows/Fonts/msyh.ttc'
BOLD = 'C:/Windows/Fonts/msyhbd.ttc'
INK='#172C3B'; MUTED='#506575'; BLUE='#2469A0'; TEAL='#087F79'; ORANGE='#AD5A24'
def font(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def canvas(h):
    im=Image.new('RGB',(1200,h),'#FAFCFD'); return im,ImageDraw.Draw(im)
def txt(d,x,y,s,size=28,color=INK,bold=False):
    d.text((x,y),s,font=font(size,bold),fill=color)
def box(d,x,y,w,h,lines,color=BLUE):
    d.rounded_rectangle((x,y,x+w,y+h),radius=14,fill='white',outline=color,width=2)
    for i,line in enumerate(lines):
        f=font(27,i==0); bounds=d.textbbox((0,0),line,font=f)
        assert bounds[2] <= w-24,(line,w,bounds)
        d.text((x+w/2,y+18+i*39),line,font=f,fill=color if i==0 else INK,anchor='mt')
def arrow(d,x1,y1,x2,y2,color=BLUE):
    d.line((x1,y1,x2,y2),fill=color,width=4)
    if y1==y2: d.polygon([(x2,y2),(x2-12,y2-7),(x2-12,y2+7)],fill=color)
    else: d.polygon([(x2,y2),(x2-7,y2-12),(x2+7,y2-12)],fill=color)

im,d=canvas(850)
txt(d,42,30,'工作流适应任务，可以发生在不同环节',38,bold=True)
txt(d,42,90,'三条并列路线；箭头表示各自流程，不表示论文之间的演进。',25,MUTED)
rows=[
    (160,'OO-Harness','先形成可复用的专门版本；部署时冻结，再按任务与轨迹选择。',BLUE,
     [['发现任务','积累执行记录'],['继承与局部修改','保留多个版本'],['部署时路由','复用基础结果或重跑']]),
    (380,'Harness²','当前任务中比较修改效果；任务结束后积累改进经验。',TEAL,
     [['参考执行','暴露具体问题'],['提出两类修订','同任务试跑对比'],['选择性合并并执行','经验进入后续任务']]),
    (600,'RRSI','给每轮修改与保留设置约束；分数更高并非唯一条件。',ORANGE,
     [['参考历史与失败','逐轮收紧修改数量'],['提出候选修改','检查泄漏与无效改动'],['评估并决定保留','考虑噪声与资源成本']])]
for y,name,desc,c,items in rows:
    txt(d,42,y,name,32,c,True); txt(d,42,y+46,desc,25)
    for x,lines in zip([42,435,828],items): box(d,x,y+93,330,105,lines,c)
    arrow(d,377,y+145,424,y+145,c); arrow(d,770,y+145,817,y+145,c)
im.save(OUT/'harness-routes.png')

fp=FontProperties(fname=FONT)
plt.rcParams.update({'font.family':fp.get_name(),'axes.unicode_minus':False,'font.size':18})
from matplotlib import font_manager
font_manager.fontManager.addfont(FONT)
fig,axes=plt.subplots(3,1,figsize=(12,9),dpi=130)
fig.patch.set_facecolor('#FAFCFD')
names=['AutomationBench · 平均部分得分','Workspace-Bench · 规则通过率均值','Toolathlon-GYM · 严格任务成功率']
# OO-Harness v1, section 5.1.1, Table 2. Compare only within each pair.
# Single ablation runs; task-only router uses a 0.7 confidence gate.
pairs=[(64.88,77.52),(40.03,40.56),(33.33,37.70)]
for ax,name,(a,b) in zip(axes,names,pairs):
    ax.set_facecolor('#FAFCFD')
    ax.barh([1,0],[a,b],height=.42,color=['#95A6B5',TEAL])
    ax.set_yticks([1,0],['只看任务','任务 + 基础执行轨迹'])
    ax.set_xlim(0,100); ax.set_xticks([0,25,50,75,100])
    ax.set_title(name,loc='left',fontproperties=fp,fontsize=20,pad=15)
    for y,v in [(1,a),(0,b)]: ax.text(v+1.2,y,f'{v:.2f}',va='center',fontsize=19,color=INK)
    ax.text(99,.5,f'+{b-a:.2f} 个百分点',ha='right',va='center',fontsize=18,color=TEAL)
    ax.spines[['top','right','left']].set_visible(False)
    ax.spines['bottom'].set_color('#C4CFD7'); ax.tick_params(axis='both',length=0,labelsize=16)
    ax.grid(axis='x',alpha=.2); ax.set_axisbelow(True)
    for label in ax.get_yticklabels(): label.set_fontproperties(fp); label.set_fontsize(18)
axes[-1].set_xlabel('各任务自身指标（%）；只在同一行内比较',fontproperties=fp,fontsize=18)
fig.suptitle('执行轨迹的价值，取决于要识别什么问题',fontproperties=fp,fontsize=25,x=.04,ha='left',y=.98,color=INK)
fig.subplots_adjust(left=.29,right=.96,top=.88,bottom=.1,hspace=.8)
fig.savefig(OUT/'routing-evidence.png',facecolor=fig.get_facecolor())
plt.close(fig)

im,d=canvas(1000)
txt(d,42,28,'记住结论，还要保住结论的来由',38,bold=True)
txt(d,42,87,'本报告自拟场景：同一段对话，未来会被问到什么并不确定。',25,MUTED)
box(d,42,140,1116,115,['原始对话：方向 A 需要持续使用设备；设备排期改变；于是改做方向 B。','后来提问：为什么改方向？如果设备恢复，原来的理由还成立吗？'],BLUE)
arrow(d,300,255,300,310,ORANGE); arrow(d,900,255,900,310,TEAL)
box(d,42,320,516,150,['压缩为事实条目','“现在做方向 B”','若只保留结论，前因与条件可能丢失'],ORANGE)
box(d,642,320,516,150,['保留原文并检索','取回相关片段及其顺序','让回答模型重建因果与条件'],TEAL)
arrow(d,300,470,300,520,ORANGE); arrow(d,900,470,900,520,TEAL)
box(d,42,530,516,112,['风险：写入时就丢失','扩大检索范围也未必能补回来'],ORANGE)
box(d,642,530,516,112,['风险：保留了却没找全','仍受检索、上下文和推理能力限制'],TEAL)
txt(d,42,690,'预算会改变取舍',31,bold=True)
txt(d,42,743,'上下文很紧',28,ORANGE,True)
txt(d,300,743,'压缩后的单元更短 → 同样空间可装入更多条证据',27)
txt(d,42,800,'上下文较宽',28,TEAL,True)
txt(d,300,800,'原始片段装得下 → 保留细节和关系的价值更容易体现',27)
txt(d,42,883,'这是对已有结果的机制解释，不是所有记忆系统都会丢失关系。',25,MUTED)
txt(d,42,927,'示意图不表示实测数据；紧预算优势仍受检索器与回答模型影响。',25,MUTED)
im.save(OUT/'memory-evidence.png')
print('\n'.join(str(OUT/name) for name in ['harness-routes.png','routing-evidence.png','memory-evidence.png']))
