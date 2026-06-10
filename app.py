{% extends "base.html" %}
{% block title %}Add Subject — SRMS{% endblock %}
{% block content %}

<div class="page-header">
  <h1>Add Subject</h1>
  <a href="{{ url_for('subjects') }}" class="btn btn-ghost">← Back</a>
</div>

<div class="form-card">
  <form method="POST">
    <div class="form-row">
      <div class="form-group">
        <label>Subject Code <span class="required">*</span></label>
        <input type="text" name="subject_code" placeholder="e.g. CS501" required maxlength="20"/>
      </div>
      <div class="form-group">
        <label>Subject Name <span class="required">*</span></label>
        <input type="text" name="subject_name" placeholder="e.g. Data Structures" required maxlength="100"/>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label>Branch <span class="required">*</span></label>
        <select name="branch" required>
          <option value="">Select Branch</option>
          {% for b in ['CSE','ECE','EEE','MECH','CIVIL','IT','AIDS','AIML'] %}
          <option value="{{ b }}">{{ b }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="form-group">
        <label>Semester <span class="required">*</span></label>
        <select name="semester" required>
          <option value="">Select Semester</option>
          {% for i in range(1,9) %}
          <option value="{{ i }}">Semester {{ i }}</option>
          {% endfor %}
        </select>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label>Max Marks</label>
        <input type="number" name="max_marks" value="100" min="1" max="200"/>
      </div>
      <div class="form-group">
        <label>Credits</label>
        <input type="number" name="credits" value="3" min="1" max="6"/>
      </div>
    </div>

    <div class="form-actions">
      <button type="submit" class="btn btn-primary">Add Subject</button>
      <a href="{{ url_for('subjects') }}" class="btn btn-ghost">Cancel</a>
    </div>
  </form>
</div>

{% endblock %}
