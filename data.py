import threading
import requests

def get_last_page_of_contest(contest_name):
    start = 1
    end = 2048
    last_page = 1
    # find last occuring leetcode rank page
    while start<=end:
        try:
            page = int((start+end)/2)
            API_URL_FMT = 'https://leetcode.com/contest/api/ranking/{}/?pagination={}&region=global'
            page_link = f'https://leetcode.com/contest/{contest_name}/ranking/{page}/'
            url = API_URL_FMT.format(contest_name, page)
            print(url)
            resp = requests.get(url).json()
            print(resp)
            objs = resp['total_rank']
            #fact we know len(objs)==0 then not valid
            if len(objs)>0:#may or may not be the last page
                last_page = page
                start = page+1
            else:
                end=  page-1
        except Exception as e:
            print('error for page',page)
            end = page-1
    print(last_page," is the last page")
    return last_page

def get_dictionary(obj_from_list, solved_progs, page_link):
    mydict = {
        # "name": obj_from_list['username'],
        "rank": obj_from_list['rank'],
        "solved": solved_progs,
        "page_link": page_link
    }
    return mydict

def iterate_pages(start,end,contest_name):
    page = start
    while page<=end:
        try:
            API_URL_FMT = 'https://leetcode.com/contest/api/ranking/{}/?pagination={}&region=global'
            page_link = f'https://leetcode.com/contest/{contest_name}/ranking/{page}/'

            url = API_URL_FMT.format(contest_name, page)
            print(url)
            resp = requests.get(url).json()
            # print(resp)
            objs = resp['total_rank']
            qns = resp['questions']
            submissions = resp['submissions']
            if len(objs) == 0:
                break

            for index,obj in enumerate(objs):
                # print(obj['username'], obj['rank'], calculate_solved_programs(obj['score']))
                obj['username'] = obj['username'].lower().strip()
                curr_obj_solved = f'{len(submissions[index])}/4'
                user_details = get_dictionary(obj, curr_obj_solved,page_link)
                total_rank_dict[obj['username']] = user_details
                # print(obj)
            print('page = ', page, ' done')
            page = page + 1
        except Exception as e:
            print(e,' so we cannot fetch details',page,url)
            #break # some times program stop executing

    for user in total_rank_dict.keys():
        print(user,total_rank_dict[user])


total_rank_dict = dict()
def get_data(CONTEST_NAME):
    contest_name = CONTEST_NAME.lower().strip().replace(' ', '-')

    last_page_of_contest = get_last_page_of_contest(contest_name= contest_name)
    thread_work_list = [[1, 250], [251, 500], [501, 750], [751, last_page_of_contest]]
    thread_list = []
    for start, end in thread_work_list:
        curr_thread = threading.Thread(target=iterate_pages,
                                       args=(start, end,contest_name,))
        thread_list.append(curr_thread)

    total_rank_dict.clear()

    thread_list[0].start()
    thread_list[1].start()
    thread_list[2].start()
    thread_list[3].start()

    thread_list[0].join()
    thread_list[1].join()
    thread_list[2].join()
    thread_list[3].join()

    return total_rank_dict
