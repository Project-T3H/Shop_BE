from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.db.models import Q
from .serializer import *
import jwt
import MySQLdb
import datetime

# Create your views here.
db = MySQLdb.connect(host='localhost', user='root', password='123456', db='shop')

# ======== USER API ======== # 
class UserView():
    # Đăng ký thông tin tài khoản
    @api_view(['POST'])
    def register(request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # print(serializer.data.id)
        # # Lưu thông tin role user
        # role_id = request.data["role_id"]
        # data2 = User_role
        # data2.role_id = role_id
        # data2.user_id = serializer.data.id
        # print(data2)
        # serializer2 = UserRoleSerializer(data2)
        # serializer2.save()

        return Response({"Message": "Success"})
    
    # Đăng nhập thông tin tài khoản
    @api_view(['POST'])
    def login(request):
        username = request.data["username"]
        password = request.data["password"]
        
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        sql = """SELECT * FROM core_user u JOIN core_user_role ur ON u.id = ur.user_id JOIN core_role r ON  r.id = ur.role_id WHERE u.username =  '""" + request.data["username"] + """'"""
        print(sql)
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)

        response.data = {
            'jwt': token,
            'user': cursor
        }
        
        return response
    
    # Đăng suất thông tin tài khoản khỏi hệ thống
    @api_view(['POST'])
    def logout(self):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        
        return response
    
    # Tìm kiếm thông tin người dùng
    @api_view(['GET'])
    def search_user(self, request):
        params = request.GET
        keyword = params.get('keyword', '')
        user_list = User.objects.filter(Q(username__icontains=keyword) | Q(email__icontains=keyword) | Q(phone__icontains=keyword))
        serializer = UserSerializer(user_list, many=True)
        return Response(serializer.data)
    
    # Liệt kê danh sách các thông tin người dùng
    @api_view(['GET'])
    def list_user(self): 
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM core_user""")
        return Response({"Message": "List of User", "User List": cursor})

    @api_view(['GET'])
    def list_user_manages(self): 
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT u.* FROM core_user u join core_user_role ur on u.id = ur.user_id
                        join core_role r on ur.role_id = r.id where r.role_name = 'ADMIN'""")
        return Response(cursor)

    @api_view(['GET'])
    def list_customer(self): 
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT u.* FROM core_user u join core_user_role ur on u.id = ur.user_id
                        join core_role r on ur.role_id = r.id where r.role_name = 'CUSTOMER'""")
        return Response(cursor)

    @api_view(['PUT'])
    def update_user(request, pk):
        try:
            data = request.data
            user = User.objects.get(pk=pk)
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.username = data["username"]
            user.email = data["email"]
            user.gender = data["gender"]
            user.date = datetime.strptime(data["date"], '%Y-%m-%d')
            user.phone = data["phone"]
            user.address = data["address"]

            user.save()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
    
    @api_view(['DELETE'])
    def delete_user(request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        

# ========  SUPPLIER API ======== # 
class SupplierView():
    # Tạo mới một Nhà cung cấp
    @api_view(['POST'])
    def create_supplier(request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
        
    # Lấy danh sách các Nhà cung cấp
    @api_view(['GET'])
    def list_supplier(request): 
        # supplier_list = Supplier.objects.all()
        # data = SupplierSerializer(supplier_list, many=True).data
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT s.id, s.supplier_name, s.phone, s.address, DATE_FORMAT(s.create_date, '%d-%m-%Y %H:%i:%s') as create_date,
                        DATE_FORMAT(s.update_date, '%d-%m-%Y %H:%i:%s') as update_date,  u.username as create_by_name,  u2.username as update_by_name  
                        FROM core_supplier s join core_user u on s.create_by_id = u.id join core_user u2 on s.update_by_id = u2.id """)
        return Response(cursor)
    
    # Tìm kiếm nhà cung cấp
    @api_view(['GET'])
    def search_supplier(request):
        params = request.GET
        keyword = params.get('keyword', '')
        supplier = Supplier.objects.filter(Q(supplier_name__icontains=keyword) | Q(phone__icontains=keyword))
        serializer = SupplierSerializer(supplier, many=True)
        return Response(serializer.data)
    
    # Cập nhật thông tin nhà cung cấp
    @api_view(["PUT"])
    def update_supplier(request, pk):
        try:
            data = request.data
            supplier = Supplier.objects.get(pk=pk)
            supplier.supplier_name = data["supplier_name"]
            supplier.phone = data["phone"]
            supplier.address = data["address"]
            
            supplier.save()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
    
    # Xóa thông tin nhà cung cấp
    @api_view(['DELETE'])
    def delete_supplier(request, pk):
        try:
            supplier = Supplier.objects.get(pk=pk)
            supplier.delete()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})


# ========  CATEGORY API ======== # 
class CategoryView():
    # Tạo mới thông tin danh mục
    @api_view(['POST'])
    def create_category(request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    # Lấy danh sách các danh mục 
    @api_view(['GET'])
    def list_category(request):
        # list_category = Category.objects.all()
        # data = CategorySerializer(list_category, many=True).data
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT c.id, c.category_name, DATE_FORMAT(c.create_date, '%d-%m-%Y %H:%i:%s') as create_date, DATE_FORMAT(c.update_date, '%d-%m-%Y %H:%i:%s') as update_date,
                            u.username as create_by_name, u2.username as update_by_name FROM core_category c join core_user u on c.create_by_id = u.id
                            join core_user u2 on c.update_by_id = u2.id """)
        return Response(cursor)
    
    # Tìm kiếm các danh mục 
    @api_view(['GET'])
    def search_category(request):
        params = request.GET
        keyword = params.get('keyword', '')
        category = Category.objects.filter(Q(category_name__icontains=keyword))
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    @api_view(['GET'])
    def get_category_id(request, pk):
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM core_category WHERE id = """ + pk)
        return Response(cursor)
    
    # Cập nhật thông tin danh mục
    @api_view(["PUT"])
    def update_category(request, pk):
        try:
            data = request.data
            category = Category.objects.get(pk=pk)
            category.category_name = data["category_name"]
            category.save()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
    
    # Xóa thông tin danh mục
    @api_view(["DELETE"])
    def delete_category(request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})

# ========  BRANCH API ======== # 
class BranchView():
    # Tạo mới nhãn hàng
    @api_view(['POST'])
    def create_branch(request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
        
    # Lấy danh sách các nhãn hàng
    @api_view(['GET'])
    def list_branch(request):
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT b.id, b.branch_name, DATE_FORMAT(b.create_date, '%d-%m-%Y %H:%i:%s') as create_date, DATE_FORMAT(b.update_date, '%d-%m-%Y %H:%i:%s') as update_date,
                            u.username as create_by_name, u2.username as update_by_name  FROM core_branch b join core_user u on b.create_by_id = u.id
                            join core_user u2 on b.update_by_id = u2.id """)
        return Response(cursor)
    
    # Xóa danh sách các nhãn hàng
    @api_view(['DELETE'])
    def delete_branch(request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
            branch.delete()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})


# ========  TICKETIMPORT API ======== # 
class TicketImportView():
    # Tạo một đơn nhập hàng
    @api_view(['POST'])
    def create_ticket(request):
        serializer = TicketImportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    # Lấy danh sách các đơn nhập hàng
    @api_view(['GET'])
    def list_ticket(request):
        list_ticket = Ticket_import.objects.all()
        data = TicketImportSerializer(list_ticket, many=True).data
        return Response(data)
    
    # Xóa các đơn nhập hàng
    @api_view(['DELETE'])
    def delete_ticketimport(request, pk):
        try:
            ticketimport = Ticket_import.objects.get(pk=pk)
            ticketimport.status = 0
            ticketimport.save()
        
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        


# ========  TICKET_IMPORT_DETAIL API ======== # 
class TicketDetailView():
    # Tạo chi tiết nhập đơn hàng mới
    @api_view(['POST'])
    def create_ticketdetail(request):
        serializer = TicketDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    # Lấy danh sách chi tiết đơn nhập hàng
    @api_view(['GET'])
    def ticketdetail_by_id(request, pk):
        ticketdetail = Ticket_Import_Detail.objects.get(pk=pk)
        data = TicketDetailSerializer(ticketdetail, many=True).data    
        return Response(data)
    
    # Cập nhật danh sách chi tiết đơn nhập hàng
    @api_view(['PUT'])
    def update_ticketdetail(request, pk):
        try:
            data = request.data
            ticketdetail = Ticket_Import_Detail.objects.get(pk=pk)
            ticketdetail.ticket_import = data['ticket_import']
            ticketdetail.product = data['product']
            ticketdetail.quantity = data['quantity']
            
            ticketdetail.save()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        
        
    # Xóa các đơn chi tiết nhập hàng
    @api_view(['DELETE'])
    def delete_ticketdetail(request, pk):
        try:
            ticketdetail = Ticket_Import_Detail.objects.get(pk=pk)
            ticketdetail.delete()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})

 
# ========  PRODUCT API ======== # 
class ProductView():
    # Tạo sản phẩm mới
    @api_view(['POST'])
    def create_product(request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=400)

    # Lấy thông tin sản phẩm theo id
    @api_view(['GET'])
    def product_by_id(request, pk):
        product = Product.objects.get(pk=pk)
        data = ProductSerializer(product).data
        
        return Response(data)

    # Lấy danh sách các sản phẩm
    @api_view(['GET'])
    def list_product(request):
        product_list = Product.objects.all()
        data = ProductSerializer(product_list, many=True).data
        return Response(data)

    @api_view(['GET'])
    def list_product_admin(request):
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""select p.id, p.product_name, p.quantity, p.price, p.sale, DATE_FORMAT(p.create_date, '%d-%m-%Y %H:%i:%s') as create_date,
                        c.category_name as category_name, b.branch_name as branch_name from core_product p join core_branch b on p.branch_id = b.id
                        join core_category c on p.category_id = c.id join core_user u on p.create_by_id = u.id """)
        return Response(cursor) 

    # Lấy danh sách các sản phẩm trong trang home
    @api_view(['GET'])
    def list_product_home(request):
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM shop.core_product limit 0, 16 """)
        return Response(cursor)

    @api_view(['GET'])
    def list_product_shop(request):
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM shop.core_product limit 0, 15 """)
        return Response(cursor)
    
    # Cập nhật thông tin sản phẩm
    @api_view(['PUT'])
    def update_product(request, pk):
        try:
            data = request.data
            product = Product.objects.get(pk=pk)
            product.branch = data['branch']
            product.category = data['category']
            product.product_name = data['product_name']
            product.quantity = data['quantity']
            product.price = data['price']
            product.sale = data['sale']
            product.rate = data['rate']
            product.description = data['description']
            product.image = data['image']
            product.content = data['content']
            product.create_by = data['create_by']
            product.update_by = data['update_by']
            
            product.save()
                        
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})

    # Xóa thông tin sản phẩm
    @api_view(['DELETE'])
    def delete_product(request, pk):
        try:
            data = request.data
            product = Product.objects.get(pk=pk)
            product.status = 0
            product.save()
        
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
    
    # Tìm kiếm thông tin sản phẩm
    @api_view(['GET'])
    def search_product(request):
        keyword = request.GET.get('keyword', '')
        product_list = Product.objects.filter(
            Q(product_name__icontains=keyword)|
            Q(category__icontains=keyword)
        )
        data = ProductSerializer(product_list, many=True).data
        
        return Response(data)

    # Lọc sản phẩm
    @api_view(['GET'])
    def filter_product(request):
        PAGE_SIZE = 5
        params = request.GET
        start = int(params.get('start', 0))
        length = int(params.get('length', PAGE_SIZE))
        branch = params.get('branch_id', '').strip()
        color = params.get('color', '')
        size = params.get('size', '')
        
        branch = branch.split(',') if branch else []
        
        product_list = Product.objects.filter(branch__in=branch, color__in=color, size__in=size)
        items = product_list[start:start+length]
        serializer = ProductSerializer(items, many=True)
        
        return Response({
            'item': serializer.data    
        })

    
# ========  PRODUCT DETAIL API ======== # 
class ProductDetailView():
    # Tạo một thông tin sản phẩm chi tiết
    @api_view(['POST'])
    def create_productdetail(request):
        serializer = ProductDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    # Cập nhật thông tin sản phẩm
    @api_view(['PUT'])
    def update_productdetail(request, pk):
        try:
            data = request.data
            productdetail = Product_Detail.objects.get(pk=pk)
            productdetail.product = data['product']
            productdetail.size = data['size']
            productdetail.color = data['color']
            
            productdetail.save()
            return Response({'success': True})
        except Exception as e:
            return ({'success': False, 'error': str(e)})
    
    
    # Xóa chi tiết sản phẩm
    @api_view(['DELETE'])
    def delete_productdetail(request, pk):
        try:
            productdetail = Product_Detail.objects.get(pk=pk)
            productdetail.delete()
            
            return Response({'success': True})
        except Exception as e:
            return ({'success': False, 'error': str(e)})

# ========  ORDERS API ======== # 
class OrdersView():
    # Tạo mới thông tin của hóa đơn
    @api_view(['POST'])
    def create_order(request):
        serializer = OrdersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        serializer.save()
        print(serializer.data)
        
        return Response(serializer.data)
    
    
    # Lấy danh sách hóa đơn theo id
    @api_view(['GET'])
    def order_by_id(request, pk):
        order = Orders.objects.get(pk=pk)
        data = OrdersSerializer(order).data
        return Response(data)
    
    # Lấy danh sách các thông tin hóa đơn
    @api_view(['GET'])
    def list_orders(self):
        # list_order = Orders.objects.all()
        # data = OrdersSerializer(list_order, many=True).data
        # return Response(data)
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT o.id, o.order_code, o.phone, o.email, o.address, o.total_price, o.status, DATE_FORMAT(o.create_date, '%d-%m-%Y %H:%i:%s') as create_date, u.username as customer_name
                            FROM core_orders o join core_user u on o.customer_name_id = u.id """)
        return Response(cursor)
    
    # Tìm kiếm thông tin hóa đơn
    @api_view(['GET'])
    def search_orders(self, request):
        params = request.GET
        keyword = params.get('keyword', '')
        order = Orders.objects.filter(Q(order_code__icontains=keyword) | Q(customer_name__icontains = keyword) | Q(phone_icontains=keyword))
        serializer = OrderItemlSerializer(order, many=True)
        
        return Response(serializer.data)
    
    # Cập nhật thông tin hóa đơn
    @api_view(['PUT'])
    def update_order(request, pk):
        try:
            data = request.data
            order = Orders.objects.get(pk=pk)
            order.order_code = data["order_code"]
            order.customer_name = data["customer_name"]
            order.phone = data["phone"]
            order.email = data["email"]
            order.address = data["address"]
            order.total_price = data["total_price"]

            order.save()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
    
    # Xóa thông tin hóa đơn
    @api_view(['DELETE'])
    def delete_order(request, pk):
        try:
            data = request.data
            order = Orders.objects.get(pk=pk)
            order.status = 0
            
            order.save()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})


# ========  TICKET_IMPORT_DETAIL API ======== # 
class OrdersItemView():
    # Tạo chi tiết hóa đơn mới
    @api_view(['POST'])
    def create_orderitem(request):
        try:
            serializer = OrderItemlSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
           
    # Cập nhật chi tiết sản phẩm
    @api_view(['PUT'])
    def update_orderitem(request, pk):
        try:
            data = request.data
            orderitem = Orders_Item.objects.get(pk=pk)
            orderitem.order = data['order']
            orderitem.product = data['product']
            orderitem.quantity = data['quantity']
            orderitem.price = data['price']
            
            orderitem.save()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})

    # Xóa chi tiết sản phẩm
    @api_view(['DELETE'])
    def delete_orderitem(request, pk):
        try:
            orderitem = Orders_Item.objects.get(pk=pk)
            orderitem.delete()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})

# ========  SIZE API ======== # 
class SizeView():
    # Lấy tất cả thông tin size
    @api_view(['GET'])
    def list_size(request):
        list_size = Size.objects.all()
        data = SizeSerializer(list_size, many=True).data
        return Response(data)

# ========  COLOR API ======== # 
class ColorView():
    # Lấy tất cả thông tin color
    @api_view(['GET'])
    def list_color(request):
        list_color = Color.objects.all()
        data = ColorSerializer(list_color, many=True).data
        return Response(data)


def paginator(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 20)
    
    page_number =  request.GET.get("page_number")
    try:
        product = paginator.page(page_number)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    
    return Response(product)