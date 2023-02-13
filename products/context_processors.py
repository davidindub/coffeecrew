from .models import Department, Category


def get_departments_for_navbar(request):
    departments = Department.objects.filter(visible_to_customers=True)

    departments_with_categories = []

    for department in departments:
        categories = Category.objects.filter(department=department)
        departments_with_categories.append({
            'name': department.name,
            'categories': categories,
        })

    return {"departments_with_categories": departments_with_categories}
