"""
URLs para la app calculator.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from calculator import views

# Router para ViewSets
router = DefaultRouter()
router.register(r'matrices', views.MatrixViewSet, basename='matrix')
router.register(r'operations', views.OperationViewSet, basename='operation')

# URLs de operaciones y stats
urlpatterns = [
    # ViewSets
    path('', include(router.urls)),
    
    # Operaciones matriciales
    path('operations/sum/', views.sum_matrices, name='sum-matrices'),
    path('operations/subtract/', views.subtract_matrices, name='subtract-matrices'),
    path('operations/multiply/', views.multiply_matrices, name='multiply-matrices'),
    path('operations/inverse/', views.inverse_matrix, name='inverse-matrix'),
    path('operations/determinant/', views.determinant_matrix, name='determinant-matrix'),
    path('operations/transpose/', views.transpose_matrix, name='transpose-matrix'),
    
    # Estadísticas
    path('stats/', views.stats_view, name='stats'),
    
    # Backup/Restore (se agregarán después)
    # path('backup/export/', views.export_backup_view, name='export-backup'),
    # path('backup/import/', views.import_backup_view, name='import-backup'),
    # path('backup/list/', views.list_backups_view, name='list-backups'),
]
