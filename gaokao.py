import requests
import csv


def generate_linkage_csv():
    url = "https://static-data.gaokao.cn/www/2.0/info/linkage.json"
    response = requests.get(url)
    data = response.json()

    # 提取JSON数据中的省份、城市和区县信息
    schools = data["data"]["school"]

    # 设置CSV文件路径
    csv_file = "schools.csv"

    # 将数据写入CSV文件
    with open(csv_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["学校", "名称"])

        for school in schools:
            school_id = school["school_id"]
            school_name = school["name"]

            writer.writerow([school_id, school_name])

    print("CSV文件生成成功！")


def generate_year_score(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == "0000":
            if "1" in data["data"]:
                min_section = data["data"]["1"]["item"][0]["min_section"]
                zslx_name = data["data"]["1"]["item"][0]["zslx_name"]
                print(zslx_name + ":" + min_section)
                return min_section
            else:
                if "2" in data["data"]:
                    min_section = data["data"]["2"]["item"][0]["min_section"]
                    zslx_name = data["data"]["2"]["item"][0]["zslx_name"]
                    print(zslx_name + ":" + min_section)
                    return min_section
                else:
                    return -1
        else:
            return -1
    else:
        print(url + "HTTP请求失败")
        return -1


def read_csv_file(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def get_school_year_history():
    url = "https://static-data.gaokao.cn/www/2.0/schoolprovincescore/140/2022/41.json";
    years = ["2023","2022", "2021", "2020"]

    filename = 'schools.csv'
    data = read_csv_file(filename)

    csv_file = "schools-years.csv"

    # 将数据写入CSV文件
    with open(csv_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        for row in data:
            results = []
            school_id = row['学校']
            school_name = row['名称']
            results.append(school_name)
            print(f"学校ID: {school_id}, 学校名称: {school_name}")
            my_url = url.replace("140", school_id)
            for year in years:
                my_year_url = my_url.replace("2022", year)
                print(my_year_url)
                position = generate_year_score(my_year_url)
                results.append(position)
            print(results)
            writer.writerow(results)


def main():
    # generate_linkage_csv()
    get_school_year_history()


if __name__ == "__main__":
    main()
