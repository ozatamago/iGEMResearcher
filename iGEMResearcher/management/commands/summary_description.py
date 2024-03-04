import openai
from django.core.management.base import BaseCommand
from iGEMResearcher.models import Team

class Command(BaseCommand):
    help = 'Generate and save summaries for Team descriptions'

    def handle(self, *args, **options):
        openai.api_key = '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'

        teams = Team.objects.all()
        for team in teams:
            if not team.description or team.description.strip() == '':
                print(f"Skipping team {team.id} due to empty description.")
                continue
            if not team.summary:
                # 3語要約のプロンプトを設定
                prompt = f"{team.description}\n\nsummary:"
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo-preview",  # チャットモデルの指定
                    messages=[
                        {"role": "system", "content": "Please summarize the iGEM project description below in ten words that symbolize the project."},
                        {"role": "user", "content": prompt},
                    ]
                )
                summary = response['choices'][0]['message']['content']
                print(summary)
                team.summary = summary
                team.save()
                print(f"Summary for {team.id} saved.")
