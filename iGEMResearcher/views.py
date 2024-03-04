from django.shortcuts import render
from .models import Team
from vectordb import vectordb  # vectordbをインポート
import openai
import json


openai.api_key = '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'

def search_teams(request):
    user_question = request.GET.get('user_question', '')
    # フリーワードの取得
    team_query = request.GET.get('team_query', '')
    description_query = request.GET.get('description_query', '')

    # 選択方式のフィルターの取得
    region = request.GET.get('region', '')
    country = request.GET.get('country', '')
    track = request.GET.get('track', '')
    year = request.GET.get('year', '')
    years = range(2004, 2024)  # これが正しく設定されているか確認
    kind = request.GET.get('kind', '')
    section = request.GET.get('section', '')

    # 最初に通常のフィルタリングを行う
    teams = Team.objects.all()
    if team_query:
        teams = teams.filter(team__icontains=team_query)
    if region:
        teams = teams.filter(region=region)
    if country:
        teams = teams.filter(country=country)
    if track:
        teams = teams.filter(track=track)
    if year:
        teams = teams.filter(year=year)
    if kind:
        teams = teams.filter(kind=kind)
    if section:
        teams = teams.filter(section=section)

    if user_question:
        # 質問の具体化
        refined_question = refine_question_with_criteria(user_question, region, track, year, kind, section, description_query)

        region_options = ["Africa", "Latin America", "Asia", "Europe", "North America"]
        track_options = ["Agriculture", "Biomanufacturing", "Bioremediation", "Climate Crisis", "Diagnostics", "Environment", "High School", "Software & AI", "Therapeutics"]
        year_options = list(range(2004, 2024))  # Adjust according to your data
        kind_options = ["High School", "Commercial", "Community Lab", "Collegiate"]
        section_options = ["Undergrad", "Overgrad", "Collegiate", "High School"]

        # Call the function with the necessary arguments
        sql_conditions_json = generate_sql_query(refined_question, region_options, track_options, year_options, kind_options, section_options)

        try:
            sql_conditions_dict = json.loads(sql_conditions_json)
        except json.JSONDecodeError:
            # JSONのデコードに失敗した場合のエラーハンドリング
            sql_conditions_dict = {}

        # SQLクエリに基づくデータの絞り込み (仮の処理)
        filtered_teams = Team.objects.filter(**sql_conditions_dict)


        ids = [team.id for team in filtered_teams]
        candidates = vectordb.search(refined_question, k=10)
        print("candidates: ", candidates)

        # LLMに質問と候補を渡し、回答を得る
        answer = ask_question_to_llm(candidates, refined_question)

        return render(request, 'iGEMResearcher/search_results.html', {'user_question': user_question, 'answer': answer, 'teams': teams, 'years': years})

    else:
        if description_query:
            # vectordb.search() が QuerySet を返すと仮定して
            # ベクトル検索はIDのリストを取得してフィルタリングする
            ids = [team.id for team in teams]
            vector_results = vectordb.search(description_query, k=10)
            vector_ids = [result.metadata['id'] for result in vector_results]
            filtered_ids = set(ids) & set(vector_ids)
            teams = teams.filter(id__in=filtered_ids)

    return render(request, 'iGEMResearcher/search_results.html', {'teams': teams, 'years': years})

def refine_question_with_criteria(content, region, track, year, kind, section, search_word):
    # 条件を明確に提示するプロンプトの作成
    conditions = f"Please consider the following conditions - Region: {region}, Track: {track}, Year: {year}, Kind: {kind}, Section: {section}, Search word: {search_word}."
    prompt = f"{conditions} Using these details, refine the following question to be more specific and clear:\n\n{content}"

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": conditions},
            {"role": "user", "content": prompt},
        ]
    )

    # 改善された質問テキストを出力
    refined_question = response['choices'][0]['message']['content']
    print("refined_question: ", refined_question.strip())
    return refined_question.strip()

def generate_sql_query(content, region_options, track_options, year_options, kind_options, section_options):
    # SQLに使用可能なすべての選択肢の一覧を条件に含める
    conditions = f"Available options - Regions: {region_options}, Tracks: {track_options}, Years: {year_options}, Kinds: {kind_options}, Sections: {section_options}."
    # 質問文に適した絞り込み方をキーに対応した値でJSON形式で出力するようプロンプトを設定
    prompt = f"{conditions} Given the refined question: '{content}', output the filtering criteria in JSON format that best matches the question."

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": conditions},
            {"role": "user", "content": prompt},
        ]
    )

    # JSON形式のSQLクエリ条件を出力
    sql_query_conditions = response.choices[0].message['content'].strip()
    print("sql_query_conditions: ", sql_query_conditions)
    return sql_query_conditions

def ask_question_to_llm(candidates, refined_question):
    candidates_text = ' '.join([
        f"Team {candidate.metadata.get('team', 'Unknown')} with track {candidate.metadata.get('track', 'Unknown')} in year {candidate.metadata.get('year', 'Unknown')} and description {candidate.metadata.get('description', 'No description available')}."
        for candidate in candidates
    ])
    # Create a prompt that includes the candidates and asks the LLM to answer the refined question
    prompt = f"Given the following candidates: {candidates_text}, answer the refined question: {refined_question}"

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Please provide a detailed answer based on the candidates."},
            {"role": "user", "content": prompt},
        ]
    )

    # Extract and return the generated answer
    answer = response.choices[0].message['content'].strip()
    print("answer: ", answer)
    return answer
