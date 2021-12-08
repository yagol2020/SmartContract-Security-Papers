import os

import bibtexparser as bp
import loguru
import pandas
from bibtexparser.bparser import BibTexParser

BASE_ORIGIN_DIR = "./origin/"
ACM = BASE_ORIGIN_DIR + "acm/"
IEEE = BASE_ORIGIN_DIR + "ieee/"
SPRINGER = BASE_ORIGIN_DIR + "springer/"


class Paper:
    def __init__(self, title, year):
        self.title = title
        self.year = int(year)

    def __hash__(self):
        return hash(self.title)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self.title) == hash(other.title)
        else:
            return False


parser = BibTexParser()
result = set()


def check_paper_relate(title, abstract, year):
    if "smart contract" in title or "smart contracts" in title:
        if (
                "bug" in title or
                "bugs" in title or
                "defect" in title or
                "defects" in title or
                "vulnerability" in title or
                "vulnerabilities" in title or
                "detect" in title or ("security" in title and "analysis" in title)
        ):
            result.add(Paper(title, year))
        else:
            if ("bug" in abstract or
                    "bugs" in abstract or
                    "defect" in abstract or
                    "defects" in abstract or
                    "vulnerability" in abstract or
                    "vulnerabilities" in abstract or
                    "detect" in abstract
            ):
                result.add(Paper(title, year))
            else:
                if "ethereum" in title and "vulnerabilities" in title:
                    result.add(Paper(title, year))
                else:
                    if ("analysis" in title or "analysis" in abstract) and (
                            "security" in title or "security" in abstract):
                        loguru.logger.warning("请查看：" + title)
                    else:
                        pass
    else:
        if "smart contract" in abstract or "smart contracts" in abstract:
            if ("bug" in abstract or
                    "bugs" in abstract or
                    "defect" in abstract or
                    "defects" in abstract or
                    "vulnerability" in abstract or
                    "vulnerabilities" in abstract or
                    "detect" in abstract
            ):
                loguru.logger.warning("请查看：" + title)
            else:
                pass
        else:
            pass


def read_bib_to_list(file_path):
    bib_file = open(file_path, mode="r")
    return bp.load(bib_file, parser=parser)


def acm():
    loguru.logger.info("acm")
    for root, dirs, files in os.walk(ACM):
        for file_name in files:
            bib_file_path = os.path.join(root, file_name)
            bib_list = read_bib_to_list(bib_file_path)
            for paper in bib_list.entries:
                title = paper["title"].lower()
                abstract = paper["abstract"].lower()
                year = paper['year']
                check_paper_relate(title, abstract, year)


@loguru.logger.catch()
def ieee():
    loguru.logger.info("ieee")
    for root, dirs, files in os.walk(IEEE):
        for file_name in files:
            csv_path = os.path.join(root, file_name)
            csv_data = pandas.read_csv(csv_path)
            for index, row in csv_data.iterrows():
                title = row["Document Title"].lower()
                abstract = row["Abstract"].lower()
                year = row['Publication Year']
                check_paper_relate(title, abstract, year)


def springer():
    loguru.logger.info("springer")
    for root, dirs, files in os.walk(SPRINGER):
        for file_name in files:
            csv_path = os.path.join(root, file_name)
            csv_data = pandas.read_csv(csv_path)
            for index, row in csv_data.iterrows():
                title = row["Item Title"].lower()
                abstract = ""
                year = row['Publication Year']
                check_paper_relate(title, abstract, year)


def convert_result():
    loguru.logger.info("最终收集到的文献数量：" + str(len(result)))
    csv = open("./handled.csv", mode="w")
    csv.write("Year,Title" + "\n")
    for paper in result:
        year = str(paper.year)
        title = paper.title.replace(",", " ")
        csv.write(year + "," + title + "\n")
    csv.close()
    loguru.logger.info("写入文件成功")
    csv = pandas.read_csv("./handled.csv")
    for select_year in range(2016, 2023, 1):
        papers = csv[csv.Year == select_year]
        loguru.logger.info(str(select_year) + ": " + str(len(papers)))


def main():
    acm()
    ieee()
    springer()
    convert_result()
    pass


if __name__ == '__main__':
    main()
