# -*- coding: utf-8 -*-
"""
福杰家电子小宠物 - 桌面版 v2.0
Desktop Pet — 在任务栏上走路、跳舞、跳跃的小宠物
可以拖拽、抓取，松手会慌张落下
使用 tkinter 实现透明窗口
"""
import tkinter as tk
from tkinter import font as tkfont
import os
import sys
import random
import math

# ===================== 常量 =====================
WIN_W = 420
WIN_H = 520
PET_W = 220
PET_H = 240
FPS_MS = 66  # ~15fps
TRANSPARENT = '#010101'
GRAVITY = 0.6
WALK_SPEED = 2
BUBBLE_FRAMES = 90

# ===================== 角色数据 =====================
CHARS = {
    'yor': {
        'id': 'yor-forger', 'name': '约尔', 'folder': '约尔', 'color': '#e74c3c',
        'messages': {
            'idle': ['~', '...', '♪', '嗯~', '♪♪'],
            'happy': ['开心~', '嘿嘿', '♡', '心情好~', '✨'],
            'grabbed': ['呀啊！', '放我下来！', '好高！', '呜呜', '救命！'],
            'walk': ['散步~', '走走', '♪'],
            'dance': ['跳舞♪', '♫♪', '啦啦啦~', '♪♫'],
            'jump': ['跳！', '嗨！', '耶！'],
            'landing': ['着陆！', '站稳~', '呼~'],
            'pet': ['害羞~', '♡', '嘿嘿', '开心~'],
        }
    },
    'loid': {
        'id': 'loid-forger', 'name': '劳埃德', 'folder': '劳埃德', 'color': '#2ecc71',
        'messages': {
            'idle': ['...', '嗯', '—', '思考中', '...'],
            'happy': ['不错', '嗯', '好', '满意'],
            'grabbed': ['！', '这不好', '放我下来', '...', '！'],
            'walk': ['巡逻', '散步', '...', '任务中'],
            'dance': ['...?', '嗯?', '♪?', '...'],
            'jump': ['跳', '!', '好'],
            'landing': ['着陆', '没问题', '...', '稳'],
            'pet': ['...', '别摸了', '...嗯', '...'],
        }
    }
}

STATE_CONFIG = {
    'idle':    (['E21-neutral', 'E01-joy', 'E22-speechless'], ['P01-standing-neutral']),
    'walk':    (['E21-neutral', 'E01-joy'], ['P01-standing-neutral', 'P02-standing-attention']),
    'dance':   (['E01-joy', 'E04-laughter', 'E16-mischievous'], ['P30-victory-sign', 'P08-thumbs-up', 'P03-hands-on-hips']),
    'jump':    (['E01-joy', 'E04-laughter'], ['P08-thumbs-up', 'P30-victory-sign']),
    'grabbed': (['E05-surprise', 'E09-crying', 'E07-aggrieved', 'E33-pleading'], ['P06-wave-goodbye', 'P25-dogeza-prostrate']),
    'falling': (['E05-surprise', 'E29-confused'], ['P06-wave-goodbye']),
    'landing': (['E21-neutral', 'E34-relieved'], ['P16-seiza', 'P17-cross-legged']),
    'sit':     (['E21-neutral', 'E01-joy'], ['P16-seiza', 'P17-cross-legged']),
}


class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.char_key = 'yor'
        self.images = {}  # {char_key: [img_info, ...]}
        self.tk_images = {}  # cache: path -> PhotoImage
        self.state = 'idle'
        self.frame = 0
        self.img_idx = 0
        self.vy = 0.0
        self.ground_y = WIN_H - PET_H - 10
        self.pet_y = self.ground_y
        self.pet_x = WIN_W // 2
        self.dragging = False
        self.drag_ox = 0
        self.drag_oy = 0
        self.walk_dir = 1
        self.walk_timer = 0
        self.state_timer = 0
        self.bubble_text = ''
        self.bubble_timer = 0
        self.particles = []
        self.rotation = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.shadow_alpha = 180

        self._init_window()
        self._load_images()
        self._draw_frame()
        self._tick()
        self.root.after(3000, self._random_behavior)
        self._show_bubble(f'我是{CHARS[self.char_key]["name"]}! 你好~')

    def _init_window(self):
        self.root.title('桌面宠物')
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', TRANSPARENT)
        self.root.geometry(f'{WIN_W}x{WIN_H}')
        self._move_to_taskbar()

        self.canvas = tk.Canvas(
            self.root, width=WIN_W, height=WIN_H,
            bg=TRANSPARENT, highlightthickness=0
        )
        self.canvas.pack()

        # Mouse bindings
        self.canvas.bind('<ButtonPress-1>', self._on_press)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)
        self.canvas.bind('<Double-Button-1>', self._on_double_click)
        self.canvas.bind('<Button-3>', self._on_right_click)

    def _move_to_taskbar(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - WIN_W) // 2
        y = sh - WIN_H - 20
        self.root.geometry(f'+{x}+{y}')

    # ---------- 图片加载 ----------
    def _load_images(self):
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))

        from PIL import Image as PILImage

        for ck, ci in CHARS.items():
            self.images[ck] = []
            result_dir = os.path.join(base, ci['folder'], '成果')
            if not os.path.isdir(result_dir):
                print(f"Warning: {result_dir} not found")
                continue
            for expr_folder in os.listdir(result_dir):
                ed = os.path.join(result_dir, expr_folder)
                if not os.path.isdir(ed):
                    continue
                for fn in os.listdir(ed):
                    if not fn.lower().endswith('.png'):
                        continue
                    parts = fn.replace('.png', '').split('__')
                    if len(parts) < 4:
                        continue
                    pose = parts[1]
                    expr_slug = parts[2]
                    full_path = os.path.join(ed, fn)
                    self.images[ck].append({
                        'path': full_path,
                        'expr': expr_slug,
                        'pose': pose,
                        'folder': expr_folder,
                    })
            print(f"Loaded {len(self.images[ck])} images for {ci['name']}")

    def _get_tk_image(self, path, w=PET_W, h=PET_H):
        key = (path, w, h)
        if key not in self.tk_images:
            from PIL import Image as PILImage, ImageTk
            img = PILImage.open(path)
            img = img.resize((int(w * self.scale_x), int(h * self.scale_y)), PILImage.LANCZOS)
            self.tk_images[key] = ImageTk.PhotoImage(img)
        return self.tk_images[key]

    def _get_image(self, expr_key=None, pose_key=None):
        imgs = self.images.get(self.char_key, [])
        if not imgs:
            return None
        if expr_key and pose_key:
            matches = [i for i in imgs if i['expr'].startswith(expr_key.split('-')[0]) and i['pose'] == pose_key]
            if matches:
                return random.choice(matches)
        if expr_key:
            matches = [i for i in imgs if i['expr'].startswith(expr_key.split('-')[0])]
            if matches:
                return random.choice(matches)
        if pose_key:
            matches = [i for i in imgs if i['pose'] == pose_key]
            if matches:
                return random.choice(matches)
        return random.choice(imgs)

    def _get_state_image_info(self):
        cfg = STATE_CONFIG.get(self.state, STATE_CONFIG['idle'])
        exprs, poses = cfg
        expr = exprs[self.img_idx % len(exprs)]
        pose = poses[self.img_idx % len(poses)]
        return self._get_image(expr, pose)

    # ---------- 动画循环 ----------
    def _tick(self):
        self.frame += 1
        self.state_timer += 1

        # Physics
        if self.state == 'falling':
            self.vy += GRAVITY
            self.pet_y += self.vy
            if self.pet_y >= self.ground_y:
                self.pet_y = self.ground_y
                self.state = 'landing'
                self.state_timer = 0
                self.frame = 0
                self.scale_x = 1.3
                self.scale_y = 0.7
                self._spawn_particles('land')
                self._clear_image_cache()

        # State transitions
        if self.state == 'jump' and self.state_timer > 30:
            self.state = 'falling'; self.vy = 0
        if self.state == 'landing' and self.state_timer > 15:
            self._set_state('idle')
        if self.state == 'walk' and self.state_timer > 90:
            self._set_state(random.choice(['idle', 'idle', 'dance', 'sit']))
        if self.state == 'dance' and self.state_timer > 60:
            self._set_state(random.choice(['idle', 'walk', 'jump']))
        if self.state == 'sit' and self.state_timer > 80:
            self._set_state(random.choice(['idle', 'walk']))
        if self.state == 'idle' and self.state_timer > 60:
            self._set_state(random.choice(['idle', 'walk', 'dance', 'sit']))

        # Walk movement
        if self.state == 'walk':
            self.walk_timer += 1
            if self.walk_timer % 3 == 0:
                self.img_idx += 1
                self._clear_image_cache()
            self._move_window(WALK_SPEED * self.walk_dir)

        # Jump
        if self.state == 'jump':
            t = self.state_timer / 30.0
            self.pet_y = self.ground_y - math.sin(t * math.pi) * 80
            if self.state_timer % 5 == 0:
                self.img_idx += 1; self._clear_image_cache()

        # Dance
        if self.state == 'dance':
            self.rotation = math.sin(self.frame * 0.3) * 12
            if self.state_timer % 8 == 0:
                self.img_idx += 1; self._clear_image_cache()

        # Idle breathing
        if self.state == 'idle':
            self.rotation = 0
            breath = math.sin(self.frame * 0.15) * 0.03
            self.scale_x = 1.0 + breath
            self.scale_y = 1.0 - breath
            if self.state_timer % 20 == 0:
                self.img_idx += 1; self._clear_image_cache()

        # Landing recovery
        if self.state == 'landing':
            self.rotation = 0
            t = min(1.0, self.state_timer / 15.0)
            self.scale_x = 1.0 + 0.3 * (1 - t)
            self.scale_y = 1.0 - 0.3 * (1 - t)
            self._clear_image_cache()

        # Grabbed wiggle
        if self.state == 'grabbed':
            self.rotation = math.sin(self.frame * 0.8) * 15
            if self.state_timer % 10 == 0:
                self.img_idx += 1; self._clear_image_cache()

        # Bubble countdown
        if self.bubble_timer > 0:
            self.bubble_timer -= 1

        # Particles
        self._update_particles()

        # Shadow
        if self.state in ('falling', 'jump'):
            height = max(0, self.ground_y - self.pet_y)
            self.shadow_alpha = max(30, 180 - int(height * 0.5))
        else:
            self.shadow_alpha = 180

        self._draw_frame()
        self.root.after(FPS_MS, self._tick)

    def _clear_image_cache(self):
        """Clear scaled image cache when scale changes"""
        self.tk_images.clear()

    def _random_behavior(self):
        if not self.dragging and self.state not in ('grabbed', 'falling', 'landing'):
            if random.random() < 0.3:
                self.walk_dir *= -1
            if random.random() < 0.4:
                msgs = CHARS[self.char_key]['messages']
                state_msgs = msgs.get(self.state, msgs.get('idle', ['...']))
                self._show_bubble(random.choice(state_msgs))
        self.root.after(3000, self._random_behavior)

    def _set_state(self, new_state):
        if self.state == new_state:
            return
        self.state = new_state
        self.state_timer = 0
        self.frame = 0
        self.img_idx = 0
        self.rotation = 0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self._clear_image_cache()
        if new_state not in ('falling', 'landing', 'grabbed'):
            self.pet_y = self.ground_y

    def _move_window(self, dx):
        x = self.root.winfo_x() + dx
        sw = self.root.winfo_screenwidth()
        if x + WIN_W > sw:
            self.walk_dir = -1
            x = sw - WIN_W
        elif x < 0:
            self.walk_dir = 1
            x = 0
        self.root.geometry(f'+{x}+{self.root.winfo_y()}')

    # ---------- 气泡 ----------
    def _show_bubble(self, text):
        self.bubble_text = text
        self.bubble_timer = BUBBLE_FRAMES

    # ---------- 粒子 ----------
    def _spawn_particles(self, ptype):
        emoji_map = {
            'land': ['✨', '⭐', '💫'], 'grab': ['❤', '💕', '✨'],
            'happy': ['❤', '♡', '✨', '♪'], 'feed': ['✨', '⭐', '💫'],
            'pet': ['❤', '♡', '💕'], 'play': ['✨', '⭐', '♪'],
            'praise': ['✨', '⭐', '💫'], 'gift': ['❤', '♡', '✨'],
        }
        emojis = emoji_map.get(ptype, ['✨', '⭐'])
        cx, cy = WIN_W // 2, int(self.pet_y) + PET_H // 2
        for _ in range(5):
            self.particles.append({
                'x': cx + random.randint(-30, 30),
                'y': cy + random.randint(-20, 10),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-4, -1),
                'life': 25 + random.randint(0, 15),
                'text': random.choice(emojis),
            })

    def _update_particles(self):
        alive = []
        for p in self.particles:
            p['x'] += p['vx']; p['y'] += p['vy']; p['vy'] += 0.05; p['life'] -= 1
            if p['life'] > 0:
                alive.append(p)
        self.particles = alive

    # ---------- 绘制 ----------
    def _draw_frame(self):
        c = self.canvas
        c.delete('all')

        # Shadow
        sy = self.ground_y + PET_H - 15
        sa = self.shadow_alpha // 4
        if sa > 10:
            c.create_oval(
                WIN_W//2 - 50, sy, WIN_W//2 + 50, sy + 20,
                fill=f'#{sa:02x}{sa:02x}{sa:02x}', outline=''
            )

        # Pet image
        info = self._get_state_image_info()
        if info:
            try:
                pw = int(PET_W * self.scale_x)
                ph = int(PET_H * self.scale_y)
                tk_img = self._get_tk_image(info['path'], PET_W, PET_H)
                px = (WIN_W - tk_img.width()) // 2
                py = int(self.pet_y)

                if self.rotation != 0:
                    # For rotation, we need to rotate the image
                    from PIL import Image as PILImage, ImageTk
                    img = PILImage.open(info['path']).resize((pw, ph), PILImage.LANCZOS)
                    rotated = img.rotate(self.rotation, expand=True, resample=PILImage.BICUBIC)
                    tk_img = ImageTk.PhotoImage(rotated)
                    px = (WIN_W - tk_img.width()) // 2
                    py = int(self.pet_y) - (tk_img.height() - ph) // 2

                # Flip for walk direction
                if self.walk_dir < 0 and self.state in ('walk', 'idle', 'dance'):
                    from PIL import Image as PILImage, ImageTk
                    if self.rotation != 0:
                        img = PILImage.open(info['path']).resize((pw, ph), PILImage.LANCZOS)
                        img = img.rotate(self.rotation, expand=True, resample=PILImage.BICUBIC)
                    else:
                        img = PILImage.open(info['path']).resize((pw, ph), PILImage.LANCZOS)
                    flipped = img.transpose(PILImage.FLIP_LEFT_RIGHT)
                    tk_img = ImageTk.PhotoImage(flipped)
                    px = (WIN_W - tk_img.width()) // 2

                # Keep reference
                self._current_tk_img = tk_img
                c.create_image(px, py, image=tk_img, anchor='nw')
            except Exception:
                pass

        # Speech bubble
        if self.bubble_timer > 0 and self.bubble_text:
            self._draw_bubble()

        # Particles
        for p in self.particles:
            alpha = max(0, min(255, int(255 * p['life'] / 40)))
            c.create_text(p['x'], p['y'], text=p['text'], font=('Segoe UI Emoji', 14), fill='white')

        # Character indicator
        ci = CHARS[self.char_key]
        c.create_rectangle(8, 8, 60, 28, fill=ci['color'], outline='')
        c.create_oval(8, 8, 60, 28, fill=ci['color'], outline='')
        c.create_text(34, 18, text=ci['name'], fill='white', font=('Microsoft YaHei', 9, 'bold'))

    def _draw_bubble(self):
        c = self.canvas
        text = self.bubble_text
        bx = WIN_W // 2
        by = int(self.pet_y) - 30
        alpha = min(220, self.bubble_timer * 4)

        # Simple bubble background
        tw = len(text) * 10 + 20
        c.create_rectangle(bx - tw//2, by - 15, bx + tw//2, by + 10,
                           fill='white', outline='#cccccc', width=1)
        # Tail
        c.create_polygon(bx - 5, by + 10, bx + 5, by + 10, bx, by + 20,
                         fill='white', outline='#cccccc', width=1)
        # Cover tail top line
        c.create_line(bx - 4, by + 10, bx + 4, by + 10, fill='white', width=2)
        # Text
        c.create_text(bx, by - 2, text=text, fill='#333333', font=('Microsoft YaHei', 10))

    # ---------- 鼠标交互 ----------
    def _is_on_pet(self, x, y):
        px = (WIN_W - PET_W) // 2
        py = int(self.pet_y)
        return px <= x <= px + PET_W and py <= y <= py + PET_H

    def _on_press(self, event):
        if self._is_on_pet(event.x, event.y):
            self.dragging = True
            self.drag_ox = event.x
            self.drag_oy = event.y
            self._set_state('grabbed')
            self.vy = 0
            msgs = CHARS[self.char_key]['messages'].get('grabbed', ['!'])
            self._show_bubble(random.choice(msgs))
            self._spawn_particles('grab')

    def _on_drag(self, event):
        if self.dragging:
            gx = self.root.winfo_x() + event.x - self.drag_ox
            gy = self.root.winfo_y() + event.y - self.drag_oy
            self.root.geometry(f'+{gx}+{gy}')

    def _on_release(self, event):
        if self.dragging:
            self.dragging = False
            self.state = 'falling'
            self.vy = 0
            self.state_timer = 0
            self._show_bubble('!')

    def _on_double_click(self, event):
        if self._is_on_pet(event.x, event.y):
            self._set_state('dance')
            msgs = CHARS[self.char_key]['messages'].get('happy', ['♪'])
            self._show_bubble(random.choice(msgs))
            self._spawn_particles('happy')

    def _on_right_click(self, event):
        if not self._is_on_pet(event.x, event.y):
            return
        menu = tk.Menu(self.root, tearoff=0, bg='#1e1e32', fg='white',
                       activebackground='#3a3a5c', activeforeground='white',
                       font=('Microsoft YaHei', 11))
        menu.add_command(label='🍱 喂食', command=lambda: self._do_action('feed'))
        menu.add_command(label='🤚 摸头', command=lambda: self._do_action('pet'))
        menu.add_command(label='🎮 玩耍', command=lambda: self._do_action('play'))
        menu.add_command(label='👍 夸奖', command=lambda: self._do_action('praise'))
        menu.add_command(label='🎁 礼物', command=lambda: self._do_action('gift'))
        menu.add_separator()
        menu.add_command(label='🔄 切换角色', command=self._switch_char)
        menu.add_separator()
        menu.add_command(label='❌ 退出', command=self._quit)
        menu.tk_popup(event.x_root, event.y_root)

    def _do_action(self, action):
        if self.dragging:
            return
        texts = {'feed': '好吃~', 'pet': '害羞~', 'play': '好玩!', 'praise': '得意~', 'gift': '惊喜!'}
        self._show_bubble(texts.get(action, '~'))
        self._set_state('dance')
        self._spawn_particles(action)

    def _switch_char(self):
        self.char_key = 'loid' if self.char_key == 'yor' else 'yor'
        self._clear_image_cache()
        self._show_bubble(f'我是{CHARS[self.char_key]["name"]}!')
        self._set_state('idle')

    def _quit(self):
        self.root.destroy()
        sys.exit(0)

    def run(self):
        self.root.mainloop()


# ===================== 入口 =====================
if __name__ == '__main__':
    pet = DesktopPet()
    pet.run()
