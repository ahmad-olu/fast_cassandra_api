import uuid
from fastapi import Depends, status, APIRouter,UploadFile
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client('s3')

router = APIRouter(
    prefix="/image_upload",
    tags=['image_upload']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=list)
async def upload_post_images(files: list[UploadFile]):
#async def upload_images(files: List[UploadFile], current_user: int = Depends(oauth2.get_current_user)):
#        
    return [upload_file(file.file, 'post_images') for file in files]

@router.post("/single_image", status_code=status.HTTP_201_CREATED,response_model=list)
async def upload_post_image(file: UploadFile):
#async def upload_images(file: UploadFile, current_user: int = Depends(oauth2.get_current_user)):
#        
    return upload_file(file.file,'post_images')

@router.post("/profile", status_code=status.HTTP_201_CREATED,response_model=list)
async def profile_image(url: str,file: UploadFile):
#async def upload_images(file: UploadFile, current_user: int = Depends(oauth2.get_current_user)):
#        
    return upload_file(file.file,'profile_images')

def upload_file(file,image_location, bucket_name = 'geat-dev-test', object_name=None):
    image_id = f'{image_location}/{uuid.uuid4()}.jpeg'
    region = "s3.eu-west-2"
    try:
        s3_client.upload_fileobj(file,bucket_name,image_id)
        return f"https://{bucket_name}.{region}.amazonaws.com/{image_id}"    
    except ClientError as e:
        return ''


#todo!! for the userProfileImage
# Future<String> uploadProfileImage({
#     required String? url,
#     required File? image,
#   }) async {
#     var imageId = const Uuid().v4();

#     // Update user profile image.
#     if (url != null) {
#       if (url.isNotEmpty) {
#         final exp = RegExp(r'userProfile_(.*).jpg');
#         imageId = exp.firstMatch(url)![1]!;
#       }
#     }

#     final downloadUrl = await _uploadImage(
#       image: image!,
#       ref: 'images/users/userProfile_$imageId.jpg',
#     );
#     return downloadUrl;
#   }