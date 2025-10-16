import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useAuth } from '@/contexts/AuthContext';
import { usePosts, Post } from '@/hooks/usePosts';
import { PostForm } from '@/components/PostForm';
import { useToast } from '@/components/ui/use-toast';
import { CommentBox } from '@/components/CommentBox';
import { useComments } from '@/hooks/useComments';
import { useProfile } from '@/hooks/useProfile';
import { Input } from '@/components/ui/input';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { 
  LogOut, 
  Plus, 
  Edit, 
  Trash2, 
  FileText, 
  User,
  Calendar,
  TrendingUp,
  Search
} from 'lucide-react';

export const Dashboard = () => {
  const { logout, username, userId } = useAuth();
  const { posts, loading, deletePost } = usePosts();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingPost, setEditingPost] = useState<Post | null>(null);
  const { toast } = useToast();
  const { uploadProfilePhoto, getProfilePhoto, loading: profileLoading } = useProfile();
  const [profilePhoto, setProfilePhoto] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const handleEdit = (post: Post) => {
    setEditingPost(post);
    setShowCreateForm(true);
  };

  const handleCloseForm = () => {
    setShowCreateForm(false);
    setEditingPost(null);
  };

  const handleDelete = async (postId: number) => {
    await deletePost(postId);
  };

  const handleProfilePhotoUpload = async (file: File) => {
    if (!username) return;
    const photoUrl = await uploadProfilePhoto(file, username);
    if (photoUrl) {
      setProfilePhoto(photoUrl);
    }
  };

  // Load existing profile photo on component mount
  useEffect(() => {
    const loadProfilePhoto = async () => {
      if (username) {
        const photoUrl = await getProfilePhoto(username);
        if (photoUrl) {
          setProfilePhoto(photoUrl);
        }
      }
    };
    loadProfilePhoto();
  }, [username, getProfilePhoto]);

  // Filter posts based on search term
  const filteredPosts = posts.filter(post => 
    post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (showCreateForm) {
    return (
      <PostForm
        post={editingPost}
        onClose={handleCloseForm}
        onSuccess={handleCloseForm}
      />
    );
  }

  return (
    <div className="min-h-screen bg-secondary-gradient">
      {/* Header */}
      <header className="border-b border-border bg-card/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 bg-primary-gradient rounded-xl flex items-center justify-center">
              <FileText className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Blog CMS</h1>
              <p className="text-sm text-muted-foreground">Content Management System</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 px-4 py-2 bg-accent-gradient rounded-lg border border-border">
              {profilePhoto ? (
                <img 
                  src={profilePhoto} 
                  alt="Profile" 
                  className="w-6 h-6 rounded-full object-cover"
                />
              ) : (
                <User className="w-4 h-4 text-foreground" />
              )}
              <span className="text-sm font-medium text-foreground">{username}</span>
            </div>
            <label className="cursor-pointer px-3 py-2 rounded-md border border-border bg-muted/30 text-sm text-foreground hover:bg-muted transition-smooth">
              {profileLoading ? 'Enviando...' : 'Foto'}
              <input
                type="file"
                accept="image/*"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleProfilePhotoUpload(file);
                }}
                className="hidden"
                disabled={profileLoading}
              />
            </label>
            <Button
              onClick={logout}
              variant="outline"
              size="sm"
              className="flex items-center space-x-2 hover:bg-destructive hover:text-destructive-foreground transition-smooth"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8 space-y-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-card/80 backdrop-blur-sm border-border shadow-soft">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total Posts
              </CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">{posts.length}</div>
              <p className="text-xs text-muted-foreground flex items-center mt-2">
                <TrendingUp className="w-3 h-3 mr-1" />
                Published articles
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card/80 backdrop-blur-sm border-border shadow-soft">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Author
              </CardTitle>
              <User className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold text-foreground">{username}</div>
              <p className="text-xs text-muted-foreground flex items-center mt-2">
                <Calendar className="w-3 h-3 mr-1" />
                Content creator
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card/80 backdrop-blur-sm border-border shadow-soft">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Quick Actions
              </CardTitle>
              <Plus className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <Button
                onClick={() => setShowCreateForm(true)}
                className="w-full bg-primary-gradient hover:opacity-90 transition-smooth font-semibold shadow-elegant"
              >
                <Plus className="w-4 h-4 mr-2" />
                New Post
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Posts Section */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-3xl font-bold text-foreground">Your Posts</h2>
              <p className="text-muted-foreground mt-1">Manage your blog content</p>
            </div>
            <Button
              onClick={() => setShowCreateForm(true)}
              className="bg-primary-gradient hover:opacity-90 transition-smooth font-semibold shadow-elegant"
            >
              <Plus className="w-5 h-5 mr-2" />
              Create New Post
            </Button>
          </div>

          {/* Search Filter */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              type="text"
              placeholder="Buscar posts por título ou descrição..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-card/50 border-border"
            />
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <Card key={i} className="bg-card/80 backdrop-blur-sm border-border animate-pulse">
                  <CardHeader>
                    <div className="h-6 bg-muted rounded-md"></div>
                    <div className="h-4 bg-muted rounded-md w-3/4"></div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="h-4 bg-muted rounded-md"></div>
                      <div className="h-4 bg-muted rounded-md w-5/6"></div>
                      <div className="flex justify-between">
                        <div className="h-8 bg-muted rounded-md w-16"></div>
                        <div className="h-8 bg-muted rounded-md w-16"></div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : filteredPosts.length === 0 ? (
            <Card className="bg-card/80 backdrop-blur-sm border-border shadow-soft">
              <CardContent className="flex flex-col items-center justify-center py-12 space-y-4">
                <div className="w-16 h-16 bg-muted/30 rounded-full flex items-center justify-center">
                  <FileText className="w-8 h-8 text-muted-foreground" />
                </div>
                <div className="text-center space-y-2">
                  <h3 className="text-xl font-semibold text-foreground">
                    {searchTerm ? 'Nenhum post encontrado' : 'No posts yet'}
                  </h3>
                  <p className="text-muted-foreground max-w-md">
                    {searchTerm 
                      ? `Nenhum post encontrado para "${searchTerm}". Tente outro termo de busca.`
                      : 'Start creating amazing content for your blog. Click the button below to write your first post.'
                    }
                  </p>
                </div>
                {!searchTerm && (
                  <Button
                    onClick={() => setShowCreateForm(true)}
                    className="bg-primary-gradient hover:opacity-90 transition-smooth font-semibold shadow-elegant"
                  >
                    <Plus className="w-5 h-5 mr-2" />
                    Write Your First Post
                  </Button>
                )}
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPosts.map((post) => (
                <Card key={post.id} className="bg-card/80 backdrop-blur-sm border-border shadow-soft hover:shadow-elegant transition-smooth group">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <CardTitle className="text-lg font-bold text-foreground line-clamp-2 group-hover:text-primary transition-smooth">
                          {post.title}
                        </CardTitle>
                        <CardDescription className="flex items-center space-x-2 mt-2">
                          <Badge variant="outline" className="text-xs">
                            {post.name}
                          </Badge>
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="space-y-4">
                    <p className="text-sm text-muted-foreground line-clamp-3">
                      {post.description}
                    </p>
                    
                    <div className="flex items-center justify-between pt-4 border-t border-border">
                      <Button
                        onClick={() => handleEdit(post)}
                        variant="outline"
                        size="sm"
                        className="flex items-center space-x-1 hover:bg-primary hover:text-primary-foreground transition-smooth"
                      >
                        <Edit className="w-3 h-3" />
                        <span>Edit</span>
                      </Button>
                      
                      <AlertDialog>
                        <AlertDialogTrigger asChild>
                          <Button
                            variant="outline"
                            size="sm"
                            className="flex items-center space-x-1 hover:bg-destructive hover:text-destructive-foreground transition-smooth"
                          >
                            <Trash2 className="w-3 h-3" />
                            <span>Delete</span>
                          </Button>
                        </AlertDialogTrigger>
                        <AlertDialogContent className="bg-card border-border">
                          <AlertDialogHeader>
                            <AlertDialogTitle className="text-foreground">Delete Post</AlertDialogTitle>
                            <AlertDialogDescription className="text-muted-foreground">
                              Are you sure you want to delete "{post.title}"? This action cannot be undone.
                            </AlertDialogDescription>
                          </AlertDialogHeader>
                          <AlertDialogFooter>
                            <AlertDialogCancel className="hover:bg-muted">Cancel</AlertDialogCancel>
                            <AlertDialogAction
                              onClick={() => handleDelete(post.id)}
                              className="bg-destructive hover:bg-destructive/90 text-destructive-foreground"
                            >
                              Delete
                            </AlertDialogAction>
                          </AlertDialogFooter>
                        </AlertDialogContent>
                      </AlertDialog>
                    </div>

                    {/* Comments list and input */}
                    <CommentsSection postId={post.id} postTitle={post.title} currentUserPhoto={profilePhoto} />
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

const CommentsSection = ({ postId, postTitle, currentUserPhoto }: { postId: number; postTitle: string; currentUserPhoto: string | null }) => {
  const { comments, addComment, deleteComment, loading } = useComments(postId);
  const { toast } = useToast();
  const { username } = useAuth();
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  return (
    <>
    <div className="space-y-4">
      <div className="space-y-2">
        <h4 className="text-sm font-semibold text-muted-foreground">Comentários</h4>
        {comments.length === 0 ? (
          <div className="text-xs text-muted-foreground">Seja o primeiro a comentar.</div>
        ) : (
          <div className="space-y-2">
            {comments.map((c) => (
              <div key={c.id} className="p-3 rounded-md border border-border bg-card/50">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center overflow-hidden">
                    {c.author === username && currentUserPhoto ? (
                      <img 
                        src={currentUserPhoto} 
                        alt={c.author || "Usuário"} 
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <User className="w-3 h-3 text-muted-foreground" />
                    )}
                  </div>
                  <span className="text-xs text-muted-foreground font-medium">{c.author || "Usuário"}</span>
                </div>
                <div className="text-sm text-foreground break-words">{c.content}</div>
                {"attachment_url" in c && c.attachment_url ? (
                  <div className="mt-2 flex gap-2">
                    <button
                      onClick={() => setPreviewUrl(String(c.attachment_url))}
                      className="text-xs px-2 py-1 rounded-md border border-border bg-muted/40 hover:bg-muted transition-smooth"
                    >
                      Ver anexo
                    </button>
                    <button
                      onClick={async () => { 
                        if (confirm('Remover anexo? O comentário permanecerá.')) {
                          // TODO: implementar remoção apenas do anexo
                        }
                      }}
                      className="text-xs px-2 py-1 rounded-md border border-border bg-muted/40 hover:bg-destructive hover:text-destructive-foreground transition-smooth"
                    >
                      Remover anexo
                    </button>
                  </div>
                ) : null}
                <div className="flex items-center justify-between mt-2">
                  <div className="text-xs text-muted-foreground">{new Date(c.created_at).toLocaleString()}</div>
                  <button
                    onClick={async () => { await deleteComment(c.id); }}
                    className="text-xs px-2 py-1 rounded-md border border-border hover:bg-destructive hover:text-destructive-foreground transition-smooth"
                  >
                    Remover
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="pt-1">
        <CommentBox
          placeholder="Escreva um comentário"
          submitLabel={loading ? 'Enviando...' : 'Comentar'}
          submittingText="Enviando..."
          onSubmit={async (text, file) => {
            const ok = await addComment(text, username || undefined, file || null);
            if (ok) {
              toast({ title: 'Comentário enviado', description: `Seu comentário em "${postTitle}" foi publicado.` });
            }
          }}
        />
      </div>
    </div>
    <AttachmentPreviewDialog url={previewUrl} onClose={() => setPreviewUrl(null)} />
    </>
  );
};

const AttachmentPreviewDialog = ({ url, onClose }: { url: string | null; onClose: () => void }) => {
  if (!url) return null;
  const lower = url.toLowerCase();
  const isImage = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"].some(ext => lower.endsWith(ext));
  const isPdf = lower.endsWith('.pdf');

  return (
    <Dialog open={!!url} onOpenChange={(open) => { if (!open) onClose(); }}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>Pré-visualização do anexo</DialogTitle>
        </DialogHeader>
        <div className="w-full max-h-[70vh] overflow-auto">
          {isImage ? (
            <img src={url} alt="preview" className="max-w-full h-auto rounded-md" />
          ) : isPdf ? (
            <iframe src={url} className="w-full h-[70vh] rounded-md" />
          ) : (
            <a href={url} target="_blank" rel="noreferrer" className="text-primary underline text-sm">Abrir anexo</a>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};