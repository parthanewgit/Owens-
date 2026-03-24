import logging
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class LearningRoadmapAgent:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def generate_roadmap(self, missing_skills: list[str]) -> dict:
        """Generate 6-week learning roadmap for missing skills"""
        
        logger.info(f"Generating roadmap for {len(missing_skills)} missing skills")
        
        skills_text = ", ".join(missing_skills)
        
        prompt = f"""Create a comprehensive 6-week learning roadmap to acquire these skills:
{skills_text}

Respond with JSON with this EXACT structure:
{{
  "week_1_topic": "string",
  "week_1_resources": ["resource1", "resource2"],
  "week_1_project": "project name",
  "week_2_topic": "string",
  "week_2_resources": ["resource1", "resource2"],
  "week_2_project": "project name",
  "week_3_topic": "string",
  "week_3_resources": ["resource1", "resource2"],
  "week_3_project": "project name",
  "week_4_topic": "string",
  "week_4_resources": ["resource1", "resource2"],
  "week_4_project": "project name",
  "week_5_topic": "string",
  "week_5_resources": ["resource1", "resource2"],
  "week_5_project": "project name",
  "week_6_topic": "string",
  "week_6_resources": ["resource1", "resource2"],
  "week_6_project": "project name",
  "overall_resources": ["resource1", "resource2"],
  "portfolio_projects": ["project1", "project2"]
}}"""
        
        # Simplified flat schema (much better compatibility with OpenAI)
        response_schema = {
            "type": "object",
            "properties": {
                "week_1_topic": {"type": "string"},
                "week_1_resources": {"type": "array", "items": {"type": "string"}},
                "week_1_project": {"type": "string"},
                "week_2_topic": {"type": "string"},
                "week_2_resources": {"type": "array", "items": {"type": "string"}},
                "week_2_project": {"type": "string"},
                "week_3_topic": {"type": "string"},
                "week_3_resources": {"type": "array", "items": {"type": "string"}},
                "week_3_project": {"type": "string"},
                "week_4_topic": {"type": "string"},
                "week_4_resources": {"type": "array", "items": {"type": "string"}},
                "week_4_project": {"type": "string"},
                "week_5_topic": {"type": "string"},
                "week_5_resources": {"type": "array", "items": {"type": "string"}},
                "week_5_project": {"type": "string"},
                "week_6_topic": {"type": "string"},
                "week_6_resources": {"type": "array", "items": {"type": "string"}},
                "week_6_project": {"type": "string"},
                "overall_resources": {"type": "array", "items": {"type": "string"}},
                "portfolio_projects": {"type": "array", "items": {"type": "string"}}
            },
            "required": [
                "week_1_topic", "week_1_resources", "week_1_project",
                "week_2_topic", "week_2_resources", "week_2_project",
                "week_3_topic", "week_3_resources", "week_3_project",
                "week_4_topic", "week_4_resources", "week_4_project",
                "week_5_topic", "week_5_resources", "week_5_project",
                "week_6_topic", "week_6_resources", "week_6_project",
                "overall_resources", "portfolio_projects"
            ]
        }
        
        result = self.llm_service.generate_structured_response(
            prompt,
            response_schema,
            temperature=0.6,
            max_tokens=3000
        )
        
        # Transform flat response back to nested structure for compatibility
        roadmap = {
            "roadmap": {
                "week_1": {
                    "topic": result.get("week_1_topic", ""),
                    "resources": result.get("week_1_resources", []),
                    "mini_project": result.get("week_1_project", "")
                },
                "week_2": {
                    "topic": result.get("week_2_topic", ""),
                    "resources": result.get("week_2_resources", []),
                    "mini_project": result.get("week_2_project", "")
                },
                "week_3": {
                    "topic": result.get("week_3_topic", ""),
                    "resources": result.get("week_3_resources", []),
                    "mini_project": result.get("week_3_project", "")
                },
                "week_4": {
                    "topic": result.get("week_4_topic", ""),
                    "resources": result.get("week_4_resources", []),
                    "mini_project": result.get("week_4_project", "")
                },
                "week_5": {
                    "topic": result.get("week_5_topic", ""),
                    "resources": result.get("week_5_resources", []),
                    "mini_project": result.get("week_5_project", "")
                },
                "week_6": {
                    "topic": result.get("week_6_topic", ""),
                    "resources": result.get("week_6_resources", []),
                    "mini_project": result.get("week_6_project", "")
                }
            },
            "resources": result.get("overall_resources", []),
            "mini_projects": result.get("portfolio_projects", [])
        }
        
        logger.info("Learning roadmap generation complete")
        
        return roadmap
