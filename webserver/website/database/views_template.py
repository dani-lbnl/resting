from rest_framework import viewsets, permissions
from django.template.response import TemplateResponse
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from database.serializers import UserSerializer, ResultSerializer, ImageSerializer
from django.contrib.auth.models import User
from database.models import Result, Image
import rest_framework_filters
import django.http
from rest_framework.renderers import BrowsableAPIRenderer

# class UserViewSet(viewsets.ReadOnlyModelViewSet):

#     queryset = User.objects.all()
    
#     serializer_class = UserSerializer

class ImageFilter(rest_framework_filters.FilterSet):

    class Meta:
        model = Image
        IMAGE_FIELDS
    
class ImageViewSet(viewsets.ModelViewSet):

    filter_class = ImageFilter
    
    serializer_class = ImageSerializer

    # Might want to allow only the creator of the object may make modifications
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Image.objects.all()
    
    # def get_queryset(self):

    #     #if len(self.request.query_params) == 0:
    #     # probably temporary, but check that some query parameters are set. Might alternatively add a pager.
    #     # seems to not be working
    #     if self.request.path_info.rstrip('/')[-1].isalpha():
    #         # Don't send all records for nonspecific requests; to request all records, one must explicitly perform a search that does not exclude any records
    #         return Image.objects.none()
    #     else:
    #         return Image.objects.all()

class SourceThumbnailViewSet(viewsets.ReadOnlyModelViewSet):

    filter_class = ImageFilter
    
    serializer_class = ImageSerializer

    queryset = Image.objects.all()
    
    # def get_queryset(self):

    #     #if len(self.request.query_params) == 0:
    #     if self.request.path_info.rstrip('/')[-1].isalpha():
    #         # Don't send all records for nonspecific requests; to request all records, one must explicitly perform a search that does not exclude any records
    #         return Image.objects.none()
    #     else:
    #         return Image.objects.all()

    def retrieve(self,request,pk=None):

        image_root = '/srv/thumbnails/'
        # Ignore the queryset since nothing is included by default
        requested = Image.objects.get(pk=pk)
        path = image_root + requested.filename
        with open(path,'rb') as image_file:
            data = image_file.read()
        extension = requested.filename.rsplit(sep='.',maxsplit=1)[1].lower()
        if extension == 'jpg' or extension == 'jpeg':
            response = django.http.HttpResponse(data,content_type='image/jpeg')
        elif extension == 'png':
            response = django.http.HttpResponse(data,content_type='image/png')
        # Ignore the serializer since we're only sending the thumbnail
        return response

    def list(self,request):

        # This uses rest_framework/templates/rest_framework/filters/base.html to generate the query form, we want to use the same machinery in the gallery display
        # This seems awkward, but it's an easy way to build out the context dictionary that's specific to the rest_framework/templates/rest_framework/filters/base.html form
        empty_data = []
        empty_response = Response()
        renderer = BrowsableAPIRenderer()
        context = renderer.get_context(empty_data,'text/html',{'view':self,'request':request,'response':empty_response})

        # Now delete some context elements that don't apply here, based on the logic in rest_framework/templates/rest_framework/filters/base.html
        try:
            del context['allowed_methods']
            del context['options_form']
            del context['delete_form']
            del context['extra_actions']
            del context['display_edit_forms']
            del context['response_headers']['Content-Type']
        except:
            pass

        # Apply the default FilterSet
        filtered_queryset = self.filter_queryset(self.get_queryset())
        
        # Would be better to respect the default settings
        paginator = PageNumberPagination()

        # This is needed for the page navigation widget to appear
        context['paginator'] = paginator
        
        # Returns a list
        page = paginator.paginate_queryset(filtered_queryset,request)
        
        # Now add the HTML content. This is filtered through urlize_quoted_links, but is otherwise pure HTML.

        # We need to generate forms that do not contain a fixed number of input elements. Since the Django Forms class creates forms based on class definitions, this is awkward. For this reason, we are implementing the thumbnail gallery forms without using most of the Django machinery.
        
        return_string = '<form><table>\n<tbody>\n'
        # Should get this URL from URLconf if possible
        image_root = '/source_thumbnail/'
        for image in page:
            str_image_pk = str(image.pk)
            path = image_root + str_image_pk
            # Might want to have an alternative detail page
            return_string += '<tr><td><input type="checkbox" id="checkbox_' + str_image_pk + '" name="checkbox_' + str_image_pk + '" value="selected"></td><td><a href="/source/' + str_image_pk + '/"><img src="' + path + '/"></a></td></tr>\n'
        # URL syntax is as follows for strings a, b, c
        # [field]__in=a%2Cb%2Cc&...
        # Should get this URL from URLconf if possible            
        # I thought that forms are sent by POST, but this is sent by GET
        return_string += '</tbody>\n</table><input type="submit" value="View selected records" formaction="/source_thumbnail_selection/"></form>\n'
            
        context['content'] = return_string
        
        response = TemplateResponse(request,'rest_framework/api.html',context = context)        
        return response

def source_thumbnail_selection(request):
    selection_string = ""
    for key in request.GET.keys():
        splits = key.split('_')
        # Looking for objects named 'checkbox_#', where # is an natural number
        pk = splits[1]
        if splits[0] == 'checkbox' and pk.isdigit():
            if selection_string == "":
                selection_string = pk                
            else:
                selection_string += "%2C" + pk
    # This will be modified to invoke the filter
    return django.http.HttpResponseRedirect('/source/?id__in='+selection_string)

#def test(request):
#    return django.http.HttpResponse('<html><head></head><body><p>'+str(request.GET)+'</p></body></html>')

class ResultFilter(rest_framework_filters.FilterSet):

    class Meta:
        model = Result
        RESULT_FIELDS
    
class ResultViewSet(viewsets.ModelViewSet):

    filter_class = ResultFilter
    
    serializer_class = ResultSerializer

    # Might want to allow only the creator of the object may make modifications
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Result.objects.all()
    
    # def get_queryset(self):

    #     #if len(self.request.query_params) == 0:
    #     if self.request.path_info.rstrip('/')[-1].isalpha():            
    #         # Don't send all records for nonspecific requests; to request all records, one must explicitly perform a search that does not exclude any records
    #         return Result.objects.none()
    #     else:
    #         return Result.objects.all()
    
        
