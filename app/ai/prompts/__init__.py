from . import programmer, engineer, doctor, lawyer, economist

PROFESSION_PROMPTS = {
    "Программист": {
        "info": programmer.INFO_PROMPT,
        "subjects": programmer.SUBJECTS_PROMPT
    },
    "Инженер": {
        "info": engineer.INFO_PROMPT,
        "subjects": engineer.SUBJECTS_PROMPT
    },
    "Врач": {
        "info": doctor.INFO_PROMPT,
        "subjects": doctor.SUBJECTS_PROMPT
    },
    "Юрист": {
        "info": lawyer.INFO_PROMPT,
        "subjects": lawyer.SUBJECTS_PROMPT
    },
    "Экономист": {
        "info": economist.INFO_PROMPT,
        "subjects": economist.SUBJECTS_PROMPT
    }
}
