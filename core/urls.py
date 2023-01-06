from django.urls import path
from .views import *


urlpatterns = [
    
    ## =================================== ##
    # URL User 
    path('register', UserView.register),
    path('login', UserView.login),
    path('user', UserView.list_user),
    path('user-manages', UserView.list_user_manages),
    path('list-customer', UserView.list_customer),
    path('logout', UserView.logout),
    path('search-user', UserView.search_user),
    path('update-user/<pk>', UserView.update_user),
    path('delete-user/<pk>', UserView.delete_user),
    
    ## =================================== ##
    # URL Supplier
    path('create-supplier', SupplierView.create_supplier),
    path('supplier', SupplierView.list_supplier),
    path('search-supplier', SupplierView.search_supplier),
    path('update-supplier/<pk>', SupplierView.update_supplier),
    path('delete-supplier/<pk>', SupplierView.delete_supplier),
    
    ## =================================== ##
    # URL Category
    path('create-category', CategoryView.create_category),
    path('category', CategoryView.list_category),
    path('search-category', CategoryView.search_category),
    path('update-category/<pk>', CategoryView.update_category),
    path('delete-category/<pk>', CategoryView.delete_category),
    path('category/<pk>', CategoryView.get_category_id),
    
    ## =================================== ##
    # URL Branch
    path('create-branch', BranchView.create_branch),
    path('branch', BranchView.list_branch),
    path('delete-branch/<pk>', BranchView.delete_branch),
    
    ## =================================== ##
    # URL Ticket_Import
    path("create-ticketimport", TicketImportView.create_ticket),
    path("list-ticketimport", TicketImportView.list_ticket),
    path("delete-ticketimport/<pk>", TicketImportView.delete_ticketimport),
    
    ## =================================== ##
    # URL Ticket_Import_Detail
    path("create-ticketdetail", TicketDetailView.create_ticketdetail),
    path("ticketdetail/<pk>", TicketDetailView.ticketdetail_by_id),
    path("update-ticketdetail/<pk>", TicketDetailView.update_ticketdetail),
    path("delete-ticketdetail/<pk>", TicketDetailView.delete_ticketdetail),
    
    ## =================================== ##
    # URL Product
    path('create-product', ProductView.create_product),
    path('product', ProductView.list_product),
    path('update-product/<pk>', ProductView.update_product),
    path('delete-product/<pk>', ProductView.delete_product),
    path('search-product', ProductView.search_product),
    path('shop', ProductView.filter_product),
	path('list-product-home', ProductView.list_product_home),
	path('list-product-admin', ProductView.list_product_admin),
    path('product/<pk>', ProductView.product_by_id),
    path('list-product-shop', ProductView.list_product_shop),
     
    ## =================================== ##
    # URL Product_Detail
    path('create-productdetail', ProductDetailView.create_productdetail),
    path('update-productdetail/<pk>', ProductDetailView.update_productdetail),
    path('delete-productdetail/<pk>', ProductDetailView.delete_productdetail),

    ## =================================== ##
    # URL Order
    path('create-order', OrdersView.create_order),
    path('order', OrdersView.list_orders),
    path('search-order', OrdersView.search_orders),
    path('update-order/<pk>', OrdersView.update_order),
    path('delete-order/<pk>', OrdersView.delete_order),
    
    ## =================================== ##
    # URL Order_Detail
    path('create-orderitem', OrdersItemView.create_orderitem),
    path('update-orderitem/<pk>', OrdersItemView.update_orderitem),
    path('delete-orderitem/<pk>', OrdersItemView.delete_orderitem),
    
    path('list-size', SizeView.list_size),
    path('list-color', ColorView.list_color),
    
    path('paginator', paginator),
    path('order/<pk>', OrdersView.order_by_id),
]
