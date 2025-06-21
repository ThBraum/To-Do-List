import { Component, EventEmitter, Output } from '@angular/core';
import { Todo } from '../../models/todo.model';
import { TodoService } from '../../services/todo.service';

@Component({
  selector: 'app-todo-form',
  templateUrl: './todo-form.component.html'
})
export class TodoFormComponent {
  todo: Todo = { title: '', description: '' };

  @Output() todoAdded = new EventEmitter<void>();

  constructor(private todoService: TodoService) {}

  addTodo() {
    this.todoService.add(this.todo).subscribe(() => {
      this.todo = { title: '', description: '' };
      this.todoAdded.emit();
    });
  }
}
