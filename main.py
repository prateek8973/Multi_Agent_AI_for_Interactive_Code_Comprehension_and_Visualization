from crew_setup import create_crew

repo_path = input("Enter repository path: ")
query = input("Ask about the repository: ")

crew = create_crew(query,repo_path)

result = crew.kickoff()

print("\nFINAL ANSWER:\n")
print(result)