from fastapi import APIRouter, Body, FastAPI
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File, Form
import shutil
import os
import imap
import email_sender
import otp

EMAIL = ""
PASSWORD = ""
PORT = ""
HOST = ""
HOST_IMAP = ""
PORT_IMAP = ""

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()


@router.get("/test")
def test():
    return {"test": "ok"}


@router.put("/creds")
def get_creds(payload=Body(...)):
    try:
        global EMAIL, PASSWORD, PORT, HOST, HOST_IMAP, PORT_IMAP
        EMAIL = payload["email_id"]
        PASSWORD = payload["password"]
        PORT = payload["port"]
        HOST = payload["host"]
        HOST_IMAP = payload["host_imap"]
        return {
            "email": EMAIL,
            "password": PASSWORD,
            "port": PORT,
            "host": HOST,
            "host_imap": HOST_IMAP,
            "port_imap": PORT_IMAP
        }
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing key in payload: {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/emails")
def get_inbox():
    try:
        print("inside get inbox")
        mails = imap.fetch_emails(EMAIL, PASSWORD, HOST_IMAP)
        return [email.to_dict() for email in mails]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/sent_email")
def get_email(payload=Body(...)):
    try:
        pass
    except Exception as e:
        return {"status": "not ok", "error": str(e)}


@app.post("/send_email")
async def post_email(
    to: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    attachment: UploadFile = File(None),
    encryption_flag: str = Form(...),
    bodyUuid: str = Form(None),
    attachmentUuid: str = Form(None),
    key: str = Form(None),
):
    try:
        # Save attachment to 'uploads' directory
        print("enc",encryption_flag)
        file_location = None
        if attachment:
            file_location = f"uploads/{attachment.filename}"
            with open(file_location, "wb") as file_object:
                shutil.copyfileobj(attachment.file, file_object)
        print("bodyuuid", bodyUuid)

        # Process the email body based on encryption flag
        if encryption_flag == "1":
            print(f'Original is {body}')
            body = otp.encode_to_64(body)
            print(f'body is {len(body)}')
            key = key  # Assuming bodyUuid is the key for encryption
            key_fin = key * (len(body) // len(key)) + key[:(len(body) % len(key))]
            print(key)
            print(key_fin)
            print(f'Final key length is {len(key_fin)}')
            try:
                encrypted_body = otp.encrypt(body, key_fin)
                body = encrypted_body
            except:
                print("Wrong encryption")
                pass
        elif encryption_flag == "2":
            # Implement AES encryption as per your logic
            pass

        # Send the email
        email_sender.send_email_with_attachment(
            to,
            bodyUuid,
            attachmentUuid,
            file_location,
            body,
            subject,
            encryption_flag,
            # to=to, subject=subject, body=body,
            # attachment_file_path=file_location,
            # attachment_mime_type=attachment.content_type if attachment else None,
            # attachment_file_name=attachment.filename if attachment else None,
        )

        # Optional: Delete the file after sending the email
        if file_location and os.path.exists(file_location):
            os.remove(file_location)

        return {"status": "ok"}
    except Exception as e:
        # Clean up if there's an error
        if file_location and os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))


# @router.post('/send_email')
# def post_email(payload=Body(...)):
#     try:
#         if payload['flag'] == 0:
#             email_sender.send_email_with_attachment(payload)
#         elif payload['flag'] == 1:
#             body = payload.get('body', '')
#             body = otp.encrypt_to_64(body)
#             key = payload.get('key','')
#             key_fin = key*(len(body)//len(key)) + key[len(body)%len(key)]
#             encrypted_body = otp.encrypt(body,key_fin)
#             payload['body'] = encrypted_body
#             email_sender.send_email_with_attachment(payload)
#         elif payload['flag'] == 2:
#             # nimish kar aes
#             pass
#         return {'status':'ok'}
#     except Exception as e:
#         return {'status': 'not ok', 'error': str(e)}


@router.post("/decrypt")
def decrypt_email(payload=Body(...)):
    try:
        key = payload["key"]
        # encrypted_message = payload["encrypted_text"]
        print(payload["flag"])
        if payload["flag"] == 0:
            return {"message": payload.get("body", "")}
        elif payload["flag"] == 1:
            print("inside flag 1")
            body = payload.get("body", "")
            print(f'body is {body}')
            key = payload.get("key", "")
            print(f'key is {key}')
            key_fin = key * (len(body) // len(key)) + key[:(len(body) % len(key))]
            message_64 = otp.decrypt(body, key_fin)
            message = otp.decode_from_64(message_64)
            return {"message": message}
        elif payload["flag"] == 2:
            # nimish kar aes
            pass
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


app.include_router(router)
