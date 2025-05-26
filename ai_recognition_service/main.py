import openai
import json

class OpenAITrashClassifierService:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.RESPONSE_SCHEMA = {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["organic", "recyclable", "non_recyclable"],
                    "description": "Tipo de residuo según clasificación de reciclaje"
                },
                "material": {
                    "type": "string",
                    "description": "Material principal"
                },
                "approximate_weight": {
                    "type": "number",
                    "description": "Peso aproximado en libras como número decimal"
                },
                # "confidence": {
                #     "type": "string",
                #     "enum": ["high", "medium", "low"],
                #     "description": "Nivel de confianza en la clasificación"
                # }
            },
            "required": [
                "type",
                "material",
                "approximate_weight",
                # "confidence"
            ],
            "additionalProperties": False
        }
        self.response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "waste_analysis",
                "strict": True,
                "schema": self.RESPONSE_SCHEMA
            }
        }

    def analyze_waste_image(self, base64_image: str) -> dict:
        ANALYSIS_PROMPT = """
        Analiza esta imagen de residuo/basura y proporciona una respuesta JSON detallada con:
        
        1. "type": Clasifica como "organic", "recyclable", o "non_recyclable"
           - "organic": Residuos biodegradables (comida, plantas, papel sucio)
           - "recyclable": Materiales que pueden procesarse nuevamente (plástico limpio, metal, vidrio, papel limpio)
           - "non_recyclable": Residuos que van a relleno sanitario (plásticos mezclados, productos híbridos, materiales contaminados)
        
        2. "material": Material principal en español (plastico, metal, papel, vidrio, etc.)
        
        3. "approximate_weight": Peso aproximado en libras como número decimal (ej: 0.8, 1.2, 0.15)
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": ANALYSIS_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "low"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300,
                temperature=0.1,  # Low temperature for consistent results
                response_format=self.response_format
            )

            result = json.loads(response.choices[0].message.content)
            return {
                "success": True,
                "classification": result,
                "tokens_used": response.usage.total_tokens,
                "cost_estimate": response.usage.total_tokens * 0.00003  # Rough cost estimate
            }

        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Failed to parse JSON response",
                "raw_response": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }