import subprocess


def run_spark_analysis():
    try:
        result = subprocess.run(
            ["python", "../analytics/spark_analysis.py"],
            capture_output=True,
            text=True,
        )

        return {
            "status": "completed",
            "output": result.stdout,
            "error": result.stderr,
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
        }