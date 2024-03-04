from matplotlib.projections import ProjectionRegistry
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from iGEMResearcher.models import Team
from tables import Description  # 適切なパスに修正してください

class Command(BaseCommand):
    help = 'Extracts descriptions from the wiki URLs and updates the database'

    def handle(self, *args, **options):
        teams = Team.objects.all()
        for team in teams:
            if team.wiki and not team.description:
                try:
                    # 特定の年に一致する場合、descriptionを空白に設定
                    if any(year in team.wiki for year in ["2004", "2005", "2006", "2007", "2013", "2021"]):
                        team.description = ''
                    else:
                        # igem.wiki または igem.org のどちらであるかを判断
                        if "igem.wiki" in team.wiki:
                            url = team.wiki + "/description"
                        elif "igem.org" in team.wiki:
                            url = team.wiki + "/Description" if "2016" in team.wiki or "2017" in team.wiki or "2018" in team.wiki or "2019" in team.wiki or "2020" in team.wiki else team.wiki + "/Project"
                        else:
                            continue  # URLが期待する形式でない場合はスキップ
                        
                        response = requests.get(url)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        # ここで適切なセレクタを使用して説明文を抽出
                        descriptions = soup.find_all("p")
                        team.description = ' '.join(block.get_text(" ", strip=True) for block in descriptions)
                        print(team.year)
                        print(team.description)
                    
                    team.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated {team.team}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error updating {team.team}: {e}'))

# https://2023.igem.wiki/aachen/description
# https://2018.igem.org/Team:Aalto-Helsinki/Description

# 4~7, 13, 21 no
# 8~12, 14, 15 /Project
# 16~20 /Description
# 22, 23 /description

