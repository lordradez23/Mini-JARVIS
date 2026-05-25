import wikipedia
import re

def search_wikipedia(query):
    """Fetches a summary from Wikipedia."""
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "I couldn't find a clear Wikipedia entry for that."

def calculate(expression):
    """Evaluates a basic mathematical expression with conversational safety."""
    try:
        expr = expression.lower()
        expr = expr.replace("plus", "+").replace("minus", "-").replace("times", "*")
        expr = expr.replace("divided by", "/").replace("over", "/")
        expr = expr.replace("squared", "**2").replace("cubed", "**3")
        expr = expr.replace("to the power of", "**")
        
        if "percent of" in expr:
            match = re.search(r'([\d.]+)\s*percent of\s*([\d.]+)', expr)
            if match:
                percentage = float(match.group(1))
                value = float(match.group(2))
                return f"The result is {value * (percentage / 100)}."

        allowed_chars = "0123456789+-*/(). "
        filtered_expr = "".join(c for c in expr if c in allowed_chars).strip()

        if filtered_expr and any(c.isdigit() for c in filtered_expr):
            try:
                result = eval(filtered_expr, {"__builtins__": {}})
                return f"The answer is {result}."
            except ZeroDivisionError:
                return "I am unable to bend the laws of mathematics, sir. One cannot divide by zero."
        return "I require a valid mathematical expression."
    except Exception as e:
        return f"I encountered an error: {str(e)}"

def convert_units(query):
    """Basic unit conversions."""
    query = query.lower()
    match = re.search(r'(?:convert\s+)?([\d.]+)\s*([a-z]+)\s*(?:to|in)\s*([a-z]+)', query)
    
    if match:
        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(3)
        
        if from_unit in ["c", "celsius"] and to_unit in ["f", "fahrenheit"]:
            return f"{value}C is {(value * 9/5) + 32:.1f}F."
        if from_unit in ["f", "fahrenheit"] and to_unit in ["c", "celsius"]:
            return f"{value}F is {(value - 32) * 5/9:.1f}C."
        # Miles/KM
        if from_unit in ["miles", "mile"] and to_unit in ["kilometers", "km"]:
            return f"{value} miles is {value * 1.61:.2f} km."
        if from_unit in ["kilometers", "km"] and to_unit in ["miles", "mile"]:
            return f"{value} km is {value / 1.61:.2f} miles."
            
        return f"I don't have the conversion for {from_unit} to {to_unit}."
    return "Please specify the conversion."
