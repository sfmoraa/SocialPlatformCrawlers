import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
from tkcalendar import Calendar
import threading
import re

from GUI.GUI_utils import *
from GUI.Visualize import *

from Weibo.WeiboCrawlMain import WeiboKeywordCrawl
from Zhihu.ZhihuCrawlMain import ZhihuQuestionCrawl
from Bilibili.BilibiliCrawlMain import BilibiliVideoCrawl


def run_GUI():
    def start_program():
        def MainCrawling():
            update_status("开始运行程序...")

            module = option.get()
            if module == 'weibo':
                weibo_config = {
                    'search_keyword': weibo_search_keyword_entry.get(),
                    'result_save_path': weibo_save_path_entry.get(),
                    'search_date_range': [start_date_entry.get(), end_date_entry.get()],
                    'weibo_cookies': {
                        "SUB": required_cookie_entry.get(),
                    },
                    'crawl_comment': weibo_collect_comments_var.get()
                }
                code, message = check_weibo_config(weibo_config)
                update_status(message)
                if code == 0:
                    WeiboKeywordCrawl(**weibo_config, log_function=update_status)
                    update_status("【任务完成！】\n")
                else:
                    update_status("【任务已结束】\n")
            elif module == 'zhihu':
                target_questions = target_questions_entry.get("1.0", "end-1c")
                normalized_questions = re.findall(r'\d+', target_questions)
                zhihu_config = {
                    'question_number_list': normalized_questions,
                    'result_save_path': zhihu_save_path_entry.get(),
                }
                code, message = check_zhihu_config(zhihu_config)
                update_status(message)
                if code == 0:
                    ZhihuQuestionCrawl(**zhihu_config, log_function=update_status)
                    update_status("【任务完成！】\n")
                else:
                    update_status("【任务已结束】\n")
            elif module == 'bilibili':
                bilibili_config = {
                    'keyword': bilibili_search_keyword_entry.get("1.0", "end-1c"),
                    'save_dir': bilibili_save_path_entry.get(),
                    'crawl_comments': bilibili_collect_comments_var.get()
                }
                code, message = check_bilibili_config(bilibili_config)
                update_status(message)
                if code == 0:
                    BilibiliVideoCrawl(**bilibili_config, log_function=update_status)
                    update_status("【任务完成！】\n")
                else:
                    update_status("【任务已结束】\n")
            elif module == 'visualize':
                visualize_config={
                    'file_path':visualize_save_path_entry.get(),
                    'time_column': visualize_time_column_entry.get("1.0", "end-1c")
                }
                code, message,pic_save_path = check_visualize_config(visualize_config)
                update_status(message)
                if code == 0:
                    image = Image.open(pic_save_path)
                    global photo
                    photo = ImageTk.PhotoImage(image)

                    image_window = tk.Toplevel()
                    image_label = tk.Label(image_window, image=photo)
                    image_label.pack()

                    update_status("【可视化完成！】\n")
                else:
                    update_status("【任务已结束】\n")

            else:
                update_status("模块选择错误，请检查")

        thread = threading.Thread(target=MainCrawling)
        thread.start()

    def update_status(message):
        status_console.config(state=tk.NORMAL)
        status_console.insert(tk.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        status_console.config(state=tk.DISABLED)
        status_console.see(tk.END)

    def on_option_change(selected_option):
        for frame in (weibo_frame, zhihu_frame, bilibili_frame,visualize_frame):
            frame.pack_forget()
        if selected_option == 'weibo':
            weibo_frame.pack(fill='x')
        elif selected_option == 'zhihu':
            zhihu_frame.pack(fill='x')
        elif selected_option == 'bilibili':
            bilibili_frame.pack(fill='x')
        elif selected_option == 'visualize':
            visualize_frame.pack(fill='x')

    '''************************************************************
                                                          
                            主界面                          
                                                  
    ************************************************************'''
    root = tk.Tk()
    root.title("SocialPlatformCrawlers")

    option = tk.StringVar(value='weibo')
    option_frame = tk.Frame(root)
    option_frame.pack(side='top', fill='x')

    weibo_rb = tk.Radiobutton(option_frame, text="微博", variable=option, value='weibo', command=lambda: on_option_change('weibo'))
    zhihu_rb = tk.Radiobutton(option_frame, text="知乎", variable=option, value='zhihu', command=lambda: on_option_change('zhihu'))
    bilibili_rb = tk.Radiobutton(option_frame, text="B站", variable=option, value='bilibili', command=lambda: on_option_change('bilibili'))
    visualize_rb = tk.Radiobutton(option_frame, text="可视化", variable=option, value='visualize', command=lambda: on_option_change('visualize'))
    weibo_rb.pack(side='left')
    zhihu_rb.pack(side='left')
    bilibili_rb.pack(side='left')
    visualize_rb.pack(side='left')

    '''************************************************************

                            微博部分                          

    ************************************************************'''

    def browse_folder_weibo():
        filename = filedialog.askdirectory()
        weibo_save_path_entry.delete(0, tk.END)
        weibo_save_path_entry.insert(0, filename)

    weibo_frame = tk.Frame(root)
    required_cookie_entry = tk.Entry(weibo_frame, width=50)
    required_cookie_label = tk.Label(weibo_frame, text="必需的cookie: SUB")
    weibo_search_keyword_entry = tk.Entry(weibo_frame, width=50)
    weibo_search_keyword_label = tk.Label(weibo_frame, text="搜索关键词：")
    weibo_save_path_entry = tk.Entry(weibo_frame, width=50)
    weibo_save_path_button = tk.Button(weibo_frame, text="浏览...", command=browse_folder_weibo)
    save_path_label = tk.Label(weibo_frame, text="结果保存路径：")
    weibo_collect_comments_var = tk.BooleanVar(value=True)
    weibo_collect_comments_label = tk.Label(weibo_frame, text="是否收集评论：")
    weibo_collect_comments_cb = tk.Checkbutton(weibo_frame, variable=weibo_collect_comments_var)

    required_cookie_label.grid(row=0, column=0)
    required_cookie_entry.grid(row=0, column=1)
    weibo_search_keyword_label.grid(row=1, column=0)
    weibo_search_keyword_entry.grid(row=1, column=1)
    save_path_label.grid(row=2, column=0)
    weibo_save_path_entry.grid(row=2, column=1)
    weibo_save_path_button.grid(row=2, column=2)
    weibo_collect_comments_label.grid(row=3, column=0, sticky="e")
    weibo_collect_comments_cb.grid(row=3, column=1, sticky="w")

    # 添加日期选择器
    def get_start_date():
        start_date_entry.delete(0, tk.END)
        start_date_entry.insert(0, calendar.get_date())

    def get_end_date():
        end_date_entry.delete(0, tk.END)
        end_date_entry.insert(0, calendar.get_date())

    calendar = Calendar(weibo_frame, selectmode='day', date_pattern='y-mm-dd')
    calendar.grid(row=6, column=0, pady=5, columnspan=3)
    target_date_button = tk.Button(weibo_frame, text="选择开始日期", command=get_start_date)
    target_date_button.grid(row=4, column=0, sticky="ew")
    start_date_entry = tk.Entry(weibo_frame, width=50)
    start_date_entry.grid(row=4, column=1, sticky="ew")
    target_date_button = tk.Button(weibo_frame, text="选择结束日期", command=get_end_date)
    target_date_button.grid(row=5, column=0, sticky="ew")
    end_date_entry = tk.Entry(weibo_frame, width=50)
    end_date_entry.grid(row=5, column=1, sticky="ew")

    # required_cookie_entry.insert(0, "_2A25I9WR_DeRhGeFG7FQZ-CrMyTuIHXVri_m3rDV8PUJbkNB-LRPtkW1NeMOQzWA74hlqBFzu9YI637-8pP33q9xT")
    # weibo_search_keyword_entry.insert(0, "张雪峰")
    # weibo_save_path_entry.insert(0, "E:\pycharm\codes\SocialPlatformCrawlers\Results")
    # start_date_entry.insert(0, "2023-12-10")
    # end_date_entry.insert(0, '2023-12-26')
    '''************************************************************

                            知乎部分                         

    ************************************************************'''

    def browse_folder_zhihu():
        filename = filedialog.askdirectory()
        zhihu_save_path_entry.delete(0, tk.END)
        zhihu_save_path_entry.insert(0, filename)

    zhihu_frame = tk.Frame(root)
    target_questions_entry = tk.Text(zhihu_frame, width=50, height=3)
    target_questions_label = tk.Label(zhihu_frame, text="问题号（不同问题号间用空格分开）")

    zhihu_save_path_label = tk.Label(zhihu_frame, text="结果保存路径：")
    zhihu_save_path_entry = tk.Entry(zhihu_frame, width=50, )
    zhihu_save_path_button = tk.Button(zhihu_frame, text="浏览...", command=browse_folder_zhihu)

    target_questions_label.grid(row=0, column=0)
    target_questions_entry.grid(row=0, column=1)
    zhihu_save_path_label.grid(row=1, column=0)
    zhihu_save_path_entry.grid(row=1, column=1)
    zhihu_save_path_button.grid(row=1, column=2)

    '''************************************************************

                            B站部分                          

    ************************************************************'''

    def browse_folder_bilibili():
        filename = filedialog.askdirectory()
        bilibili_save_path_entry.delete(0, tk.END)
        bilibili_save_path_entry.insert(0, filename)

    bilibili_frame = tk.Frame(root)
    bilibili_search_keyword_entry = tk.Text(bilibili_frame, width=50, height=1)
    bilibili_search_keyword_label = tk.Label(bilibili_frame, text="搜索关键词")

    bilibili_collect_comments_var = tk.BooleanVar(value=True)
    bilibili_collect_comments_label = tk.Label(bilibili_frame, text="是否收集评论：")
    bilibili_collect_comments_cb = tk.Checkbutton(bilibili_frame, variable=bilibili_collect_comments_var)

    bilibili_save_path_label = tk.Label(bilibili_frame, text="结果保存路径：")
    bilibili_save_path_entry = tk.Entry(bilibili_frame, width=50)
    bilibili_save_path_button = tk.Button(bilibili_frame, text="浏览...", command=browse_folder_bilibili)

    bilibili_search_keyword_label.grid(row=0, column=0)
    bilibili_search_keyword_entry.grid(row=0, column=1)
    bilibili_collect_comments_label.grid(row=1, column=0)
    bilibili_collect_comments_cb.grid(row=1, column=1, sticky="w")
    bilibili_save_path_label.grid(row=2, column=0)
    bilibili_save_path_entry.grid(row=2, column=1)
    bilibili_save_path_button.grid(row=2, column=2)

    '''************************************************************

                                可视化部分                          

        ************************************************************'''

    def browse_folder_visualize():
        filename = filedialog.askopenfilename()
        visualize_save_path_entry.delete(0, tk.END)
        visualize_save_path_entry.insert(0, filename)

    visualize_frame = tk.Frame(root)

    visualize_save_path_label = tk.Label(visualize_frame, text="选取数据文件")
    visualize_save_path_entry = tk.Entry(visualize_frame, width=50)
    visualize_save_path_button = tk.Button(visualize_frame, text="浏览...", command=browse_folder_visualize)

    visualize_time_column_entry = tk.Text(visualize_frame, width=20, height=1)
    visualize_time_column_label = tk.Label(visualize_frame, text="时间戳在数据中列数")

    visualize_save_path_label.grid(row=0, column=0)
    visualize_save_path_entry.grid(row=0, column=1)
    visualize_save_path_button.grid(row=0, column=2)
    visualize_time_column_label.grid(row=1, column=0)
    visualize_time_column_entry.grid(row=1, column=1, sticky='w')

    '''************************************************************

                            运行                          

    ************************************************************'''

    status_frame = tk.Frame(root)
    status_frame.pack(side='bottom', fill='x')

    status_console = scrolledtext.ScrolledText(status_frame, height=20, state=tk.DISABLED)
    status_console.pack(fill='both', expand=True)

    run_button = tk.Button(status_frame, text="开始运行", command=start_program)
    run_button.pack(side='left', padx=10)

    on_option_change('weibo')  # 默认显示微博界面

    root.mainloop()
