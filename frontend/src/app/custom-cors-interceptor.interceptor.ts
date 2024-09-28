import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class CustomCorsInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Клонируем запрос, чтобы добавить новые заголовки
    const modifiedReq = req.clone({
      setHeaders: {
        'Access-Control-Allow-Origin': '*',  // Пример CORS заголовка
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      }
    });

    // Передаем измененный запрос дальше по цепочке перехватчиков
    return next.handle(modifiedReq);
  }
}