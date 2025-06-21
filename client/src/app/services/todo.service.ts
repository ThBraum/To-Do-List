import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Todo } from '../models/todo.model';

@Injectable({ providedIn: 'root' })
export class TodoService {
  private API = 'http://localhost:7071';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Todo[]> {
    return this.http.get<Todo[]>(`${this.API}/get-to-do-list`);
  }

  add(todo: Todo): Observable<Todo> {
    return this.http.post<Todo>(`${this.API}/add-to-do`, todo);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/delete-to-do-item/${id}`);
  }

  getById(id: number): Observable<Todo> {
    return this.http.get<Todo>(`${this.API}/to_to/${id}`);
  }
}
