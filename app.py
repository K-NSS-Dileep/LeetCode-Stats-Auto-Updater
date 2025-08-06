#Importing Required Libraries
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader
import requests
import json
import re
import time
import os

#class for easy access of stats
class LeetCodeStats(BaseModel):
    total_solved: str
    total_questions: str
    globalrank: str
    easy_solved: str
    easy_total:str
    medium_solved: str
    medium_total: str
    hard_solved: str
    hard_total: str
    languages_used: list

#configuration
leetcode_username = "Dileep_Karra"
graphql_url = "https://leetcode.com/graphql"
query = """query($username: String!){
                matchedUser(username: $username){
                    submitStats{
                        acSubmissionNum{
                            difficulty
                            count
                        }
                    }
                    profile{
                        ranking
                    }
                    languageProblemCount{
                        languageName
                        problemsSolved
                    }
                }
                allQuestionsCount{
                        difficulty
                        count
                }
            }"""

def fetch_leetcode_stats() -> LeetCodeStats:
    stats = LeetCodeStats(
                total_solved="0",
                total_questions="0",
                globalrank="0",
                easy_solved="0",
                easy_total="0",
                medium_solved="0",
                medium_total="0",
                hard_solved="0",
                hard_total="0",
                languages_used=[]
                )
    headers = {
        "Content-Type" : "application/json"
    }
    payload = {
        "query": query,
        "variables": {"username": leetcode_username}
    }
    try:
        response = requests.post(graphql_url, json = payload, 
                                 headers = headers)
        #raises an exception if the request fails
        #status code (200 - 299) nothing happens
        #status code (400 - 599) HTTPError exception 
        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise Exception(f"""GrpahQL Error: {data["errors"]}""")
    except Exception as e:
        #Incase of exception returing default stats
        return stats
    
    matched_user = data["data"]["matchedUser"]
    if not matched_user:
        print("User not found")
        return stats
    
    #Extracting the total questions solved
    all_questions = {item["difficulty"]: item["count"] 
                     for item in data["data"]["allQuestionsCount"]}
    total_questions = all_questions.get("All", 0)
    easy_total = all_questions.get("Easy", 0)
    medium_total = all_questions.get("Medium", 0)
    hard_total = all_questions.get("Hard", 0)


    #Extracting Count of Solved Questions
    submit_stats = {item["difficulty"]: item["count"] 
                    for item in matched_user["submitStats"]["acSubmissionNum"]}

    total_solved = submit_stats.get("All", 0)
    easy_solved = submit_stats.get("Easy", 0)
    medium_solved = submit_stats.get("Medium", 0)
    hard_solved = submit_stats.get("Hard", 0)


    #Extracting rank
    rank = matched_user["profile"]["ranking"]

    #Extracting langauges
    languages = []
    for language in matched_user["languageProblemCount"]:
        languages.append([language["problemsSolved"], language["languageName"]])
    
    #Sorting the langauges based on their count
    languages.sort(reverse = True, key = lambda x: x[0])

    #ReAssinging the values of the object
    stats.total_solved = str(total_solved)
    stats.total_questions = str(total_questions)
    stats.globalrank = str(rank)
    stats.easy_solved = str(easy_solved)
    stats.easy_total = str(easy_total)
    stats.medium_solved = str(medium_solved)
    stats.medium_total = str(medium_total)
    stats.hard_solved = str(hard_solved)
    stats.hard_total = str(hard_total)
    stats.languages_used = languages
    
    return stats


#Generating the lang count svg code
def generate_lang_count(stats: LeetCodeStats) -> str:
    output_string, y = [], 80
    #showcasing only the top 3 languages used
    for count, lang in stats.languages_used[:3]:
        output_string.append(f"""
<text x="390" y="{y}" font-family="Arial, sans-serif" font-size="20" fill="#ffffff">{lang}</text>
<text x="550" y="{y}" font-family="Arial, sans-serif" font-size="14" fill="#ffffff">{count}</text>
""")
        y += 30

    return "\n".join(output_string)

    
def generate_stats_svg(stats: LeetCodeStats) -> str:
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader = FileSystemLoader(template_dir))
    template = env.get_template('Design.svg')
    rendered_svg = template.render(stats = stats, dynamic_change = generate_lang_count(stats))
    return rendered_svg

if __name__ == '__main__':
    stats = fetch_leetcode_stats()
    print("Fetched Stats:", stats)
    
    generated_design = generate_stats_svg(stats)
    if not generated_design.strip():
        print("Generated SVG is empty. Check template or stats.")
    else:
        print("Generated SVG successfully.")
    
    svg_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Display.svg")
    print(f"Saving to {svg_file_path}")
    with open(svg_file_path, "w") as file:
        file.write(generated_design)
        print("Written in Display.svg successfully")
    
    base_url = """<img align="center"
                src ="https://raw.githubusercontent.com/K-NSS-Dileep/LeetCode-Stats-Auto-Updater/main/Display.svg?cache_bust={}"
                alt ="LeetCodeStats"
                />"""
    readme_path = os.path.join("K-NSS-Dileep", "README.md")


    with open(readme_path, "r") as file:
        content = file.read()

    timestamp = int(time.time())
    new_content = base_url.format(timestamp)
    start_tag = "<!-- LEETCODE_STATS_START -->"
    end_tag = "<!-- LEETCODE_STATS_END -->"

    # Replace content between start and end tags
    pattern = f"{start_tag}.*?{end_tag}"
    updated_content = re.sub(pattern, f"{start_tag}\n{new_content}\n{end_tag}", content, flags=re.DOTALL)

    # Write the updated content back to README.md
    with open(readme_path, "w") as file:
        file.write(updated_content)
    print('LeetCode stats updated successfully.')
 

